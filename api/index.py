import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from mysql.connector import Error as DatabaseError
from starlette.exceptions import HTTPException

from backend.config import settings
from backend.routes import cep, pedidos, produtos, usuarios


@asynccontextmanager
async def lifespan(app):
    settings()  # Valida configuração no início, sem abrir conexão permanente.
    yield


app = FastAPI(title="Dessik • API da loja", version="1.0.0", lifespan=lifespan,
              docs_url="/api/docs", redoc_url=None, openapi_url="/api/openapi.json")
origins = [value.strip() for value in os.getenv("CORS_ORIGINS", "").split(",") if value.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False,
                   allow_methods=["GET", "POST", "PUT", "DELETE"],
                   allow_headers=["Authorization", "Content-Type"])


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    if not request.url.path.startswith("/api/docs"):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' https:; connect-src 'self'; object-src 'none'; "
            "base-uri 'self'; frame-ancestors 'none'; form-action 'self'")
    return response


@app.exception_handler(HTTPException)
async def http_error(request, error):
    return JSONResponse({"mensagem": error.detail}, status_code=error.status_code, headers=error.headers)


@app.exception_handler(RequestValidationError)
async def validation_error(request, error):
    # Nunca devolva error.input: pode conter senhas enviadas pelo usuário.
    fields = [{"campo": ".".join(str(part) for part in item["loc"][1:]),
               "mensagem": item["msg"]} for item in error.errors()]
    return JSONResponse({"mensagem": "Confira os campos informados.", "erros": fields}, status_code=422)


@app.exception_handler(DatabaseError)
async def database_error(request, error):
    logging.getLogger("dessik").error("Falha MySQL: código %s", error.errno)
    if error.errno in (1205, 1213):
        return JSONResponse({"mensagem": "Operação concorrente. Atualize os dados e tente novamente."}, status_code=409)
    return JSONResponse({"mensagem": "Banco indisponível. Tente novamente mais tarde."}, status_code=503)


@app.exception_handler(Exception)
async def unexpected_error(request, error):
    logging.getLogger("dessik").error("Falha inesperada: %s", type(error).__name__)
    return JSONResponse({"mensagem": "Não foi possível concluir a operação."}, status_code=500)


@app.get("/api/health", tags=["Sistema"])
def health():
    return {"status": "ok"}


for router in (usuarios.router, produtos.router, pedidos.router, cep.router):
    app.include_router(router, prefix="/api")


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], include_in_schema=False)
def unknown_api(path: str):
    raise HTTPException(404, "Endpoint não encontrado.")


# Na Vercel, public/ é servido pela CDN. Localmente, Uvicorn serve a mesma pasta.
if os.getenv("VERCEL") != "1":
    app.mount("/", StaticFiles(directory=Path(__file__).resolve().parents[1] / "public", html=True), name="frontend")
