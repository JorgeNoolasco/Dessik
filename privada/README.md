# Dessik — back-end

Python executa as regras da loja. FastAPI expõe rotas HTTP e valida JSON com Pydantic. `mysql-connector-python` executa SQL visível. Não há ORM, Repository Pattern ou camadas de serviço.

## Executar em uma máquina nova

Instale Python 3.12 ou 3.13 e MySQL 8.0.16+ (por exemplo, MySQL Community Server com Workbench). No terminal, entre em `workspace/privada`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Não copie sobre um `.env` que você já configurou. Edite o `.env` local com os dados do **seu** banco. Não envie esse arquivo ao Git nem ao navegador.

No MySQL Workbench, crie e selecione um banco novo:

```sql
CREATE DATABASE loja_ficticia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE loja_ficticia;
```

Abra e execute `database/schema.sql` e depois `database/dados.sql` na conexão com esse banco selecionado. São quatro tabelas e 12 produtos. Rodar novamente `dados.sql` não reinicia o estoque dos IDs existentes. Use um banco novo, separado da versão antiga do repositório.

Preencha estas variáveis:

| Variável | Significado |
| --- | --- |
| `DB_HOST` | Endereço do servidor; local pode ser `127.0.0.1` |
| `DB_PORT` | Porta do servidor, geralmente `3306` |
| `DB_USER` | Usuário do banco |
| `DB_PASSWORD` | Senha desse usuário |
| `DB_NAME` | Banco selecionado, por exemplo `loja_ficticia` |
| `DB_SSL` | `false` apenas para teste local; `true` no MySQL remoto |
| `DB_SSL_CA` | Caminho do certificado CA, quando o provedor exigir |
| `JWT_SECRET` | Chave aleatória privada com pelo menos 32 bytes |
| `JWT_ALGORITHM` | `HS256` neste projeto |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Validade do token, padrão de exemplo: `60` |
| `APP_ENV` | `development` local; `production` publicado |
| `CORS_ORIGINS` | Origens permitidas, separadas por vírgula, sem `*` |

Para gerar sua chave local, execute e copie a saída para `JWT_SECRET`:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
```

Use um usuário de aplicação com SELECT, INSERT, UPDATE e DELETE apenas no banco da loja. Use sua conexão administrativa para criar tabelas, importar produtos ou promover admin.

Inicie o servidor:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Abra **http://127.0.0.1:8000**. A documentação interativa da API fica em **http://127.0.0.1:8000/api/docs**. `GET /api/health` verifica que a API está no ar; `GET /api/produtos` também verifica a conexão com o banco.

Nesta máquina, a revisão deixou uma instância local em `127.0.0.1:8000`, usando um banco `dessik_workspace` no MariaDB de testes já disponível. O `.env` local foi criado com credenciais aleatórias e não está incluído no guia nem nos arquivos públicos. Esse ambiente de revisão não é uma instalação de MySQL Community; siga as instruções acima para seu MySQL definitivo.

## Criar seu administrador

Cadastre uma conta pela interface. No MySQL Workbench, conectado ao banco correto, substitua o e-mail abaixo pelo seu e-mail cadastrado:

```sql
UPDATE usuarios SET tipo_usuario = 'admin' WHERE email = 'seu-email@example.com';
```

Atualize a página para aparecer Administração. Não existe senha padrão nem endpoint público que promova usuários. Clientes sempre nascem com `tipo_usuario = 'cliente'`. O backend rejeita campos extras enviados ao cadastro.

## Arquivos e conceitos

| Arquivo | O que faz |
| --- | --- |
| `api/index.py` | Exporta `app` para a Vercel |
| `backend/main.py` | Cadastro, login, produtos, pedidos, ViaCEP e tratamento de erros |
| `backend/database.py` | Lê o `.env` desta pasta, valida configuração e abre conexões curtas |
| `backend/auth.py` | Hash bcrypt, geração/verificação JWT e checagem de admin |
| `backend/models.py` | Converte o preço Decimal em texto para o JSON; os modelos relacionais estão no SQL |
| `backend/schemas.py` | Regras dos campos: e-mail, senha, quantidade, preço e URL de imagem |
| `database/schema.sql` | Tabelas, chaves estrangeiras e restrições |
| `database/dados.sql` | Insere os 12 produtos fictícios |
| `requirements.txt` | Bibliotecas de execução com versões fixadas |
| `tests/` | Testes funcionais e de segurança, separados da aplicação |

`with transaction() as cursor` é uma forma curta de abrir uma transação. Ao terminar, faz `commit`. Se ocorrer erro, faz `rollback`. Finalmente fecha cursor e conexão. É o único context manager de banco, para não repetir esse cuidado em todas as rotas.

Senha → bcrypt → hash → MySQL. No login, bcrypt compara a senha informada com o hash. Senha não é descriptografada. O hash recebe um salt aleatório, portanto duas senhas iguais não geram necessariamente o mesmo texto armazenado.

JWT → assinatura com `JWT_SECRET` → token temporário. A API verifica assinatura, expiração, emissor e destinatário. O ID do usuário vem do token validado. O papel admin é lido do banco, não aceito de um campo enviado pelo navegador.

ViaCEP: navegador → `GET /api/cep/{cep}` → `https://viacep.com.br` → API → formulário. Há timeout de cinco segundos, validação de oito dígitos e mensagens para CEP inexistente ou serviço indisponível. O usuário pode preencher manualmente.

## Rotas

| Método | Rota | Acesso |
| --- | --- | --- |
| POST | `/api/cadastro` | Público |
| POST | `/api/login` | Público |
| GET | `/api/me` | JWT |
| GET | `/api/gerar-senha` | Público |
| GET | `/api/cep/{cep}` | Público |
| GET | `/api/produtos` e `/api/produtos/{id}` | Público |
| POST | `/api/produtos` | Admin |
| PUT / DELETE | `/api/produtos/{id}` | Admin |
| POST | `/api/pedidos` | JWT |
| GET | `/api/pedidos` | JWT; retorna somente os próprios pedidos |

Para criar pedido, envie somente:

```json
{"itens": [{"id_produto": 2, "quantidade": 2}, {"id_produto": 3, "quantidade": 1}]}
```

Use o cabeçalho `Authorization: Bearer TOKEN_DO_LOGIN`. O valor é recalculado no banco. Tentar adicionar preço, ID de outro usuário ou papel administrativo ao corpo resulta em erro de validação. Isso evita confiar em valores que qualquer pessoa poderia alterar nas ferramentas do navegador.

## Publicar na Vercel e conectar MySQL remoto

Prepare **dois projetos**: front-end estático com Root Directory `workspace/publico` e back-end com Root Directory `workspace/privada`. No estático, use preset Other, sem comando de build e sirva a própria raiz. No back-end, a Vercel reconhece FastAPI e `api/index.py`, que exporta `app`. `vercel.json` apenas seleciona o framework, sem configurações legadas `builds`/`routes`.

1. Crie um MySQL remoto e importe os dois arquivos SQL no banco correto.
2. Configure as variáveis privadas no painel do projeto back-end, incluindo `APP_ENV=production`, `DB_SSL=true` e um `JWT_SECRET` novo.
3. Use o hostname fornecido pelo provedor em `DB_HOST`, nunca `localhost` ou `127.0.0.1` em produção. Configure porta, usuário, senha e nome conforme o provedor.
4. Habilite acesso de rede da hospedagem ao banco conforme as opções do provedor e mantenha validação do certificado TLS. Se precisar de CA própria, disponibilize o certificado e configure `DB_SSL_CA`.
5. Coloque a URL HTTPS do front-end em `CORS_ORIGINS`, sem barra final. Inclua apenas as origens necessárias; prévias com outro domínio precisam ser configuradas explicitamente.
6. Em `publico/js/api.js`, altere `API_URL` para `https://SEU-BACKEND.vercel.app/api` e publique o front-end.
7. Confira cadastro, login, ViaCEP, CRUD e compra no ambiente publicado com dados fictícios.

O `.env` não é publicado como arquivo. CORS permite a comunicação do navegador com a API, mas não substitui JWT ou autorização. O servidor local usa CSP com `connect-src 'self'`; por isso, quando mudar a API para outro domínio, hospede o front-end separadamente e configure sua política CSP para permitir exatamente essa origem. Sempre use HTTPS nos dois projetos.

Configuração conferida na [documentação oficial FastAPI na Vercel](https://vercel.com/docs/frameworks/backend/fastapi) e na [referência de vercel.json](https://vercel.com/docs/project-configuration/vercel-json). A publicação efetiva não foi realizada nesta tarefa.

## Rodar os testes

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Sem `RUN_MYSQL_TESTS=1`, os testes de integração ficam desabilitados. Os testes básicos usam configuração fictícia e não precisam de conexão. Para integração, crie um banco separado terminado em `_test`, importe o SQL e configure **todas** as variáveis `DB_*` e `JWT_SECRET` no terminal para esse banco. Nunca use o banco da apresentação ou de produção.

```powershell
$env:RUN_MYSQL_TESTS = "1"
.\.venv\Scripts\python.exe -m pytest -q
```

Os testes criam contas/produtos fictícios no banco de teste. Recrie esse banco quando quiser uma base limpa. Testam CRUD, hash, SQL parametrizado, rollback e concorrência de estoque. O arquivo `test_browser.py` é opcional: instale `playwright`, use Edge e uma API separada na porta 8001 apontando ao mesmo banco de teste; defina `RUN_BROWSER_TESTS=1` e `BROWSER_URL=http://127.0.0.1:8001` para executar o fluxo visual.

Consulte o [roteiro de apresentação e a tabela de segurança](../README.md) para os testes manuais e os resultados da revisão.
