from decimal import Decimal
import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Login(Input):
    email: EmailStr = Field(max_length=254)
    senha: str = Field(min_length=1, max_length=72)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        return value.lower()

    @field_validator("senha")
    @classmethod
    def password_bytes(cls, value):
        if len(value.encode("utf-8")) > 72:
            raise ValueError("A senha deve ter no máximo 72 bytes UTF-8.")
        return value


class Cadastro(Login):
    nome: str = Field(min_length=2, max_length=100)
    senha: str = Field(min_length=8, max_length=72)
    confirmar_senha: str = Field(min_length=8, max_length=72)
    cep: str = ""
    logradouro: str = Field(default="", max_length=150)
    bairro: str = Field(default="", max_length=100)
    cidade: str = Field(default="", max_length=100)
    estado: str = Field(default="", max_length=2)

    @field_validator("nome")
    @classmethod
    def valid_name(cls, value):
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Informe um nome com pelo menos 2 caracteres.")
        return value

    @field_validator("cep")
    @classmethod
    def valid_cep(cls, value):
        value = value.replace("-", "").strip()
        if value and not re.fullmatch(r"[0-9]{8}", value):
            raise ValueError("CEP deve conter 8 números.")
        return value

    @field_validator("estado")
    @classmethod
    def valid_state(cls, value):
        value = value.upper()
        if value and value not in "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split():
            raise ValueError("UF inválida.")
        return value

    @model_validator(mode="after")
    def matching_passwords(self):
        if self.senha != self.confirmar_senha:
            raise ValueError("As senhas não coincidem.")
        return self


class Produto(Input):
    nome: str = Field(min_length=2, max_length=120)
    descricao: str = Field(min_length=1, max_length=2000)
    categoria: str = Field(min_length=1, max_length=60)
    preco: Decimal = Field(gt=0, le=99999999.99, max_digits=10, decimal_places=2)
    quantidade_estoque: int = Field(ge=0, le=1000000, strict=True)
    imagem_url: str = Field(max_length=1000)

    @field_validator("nome", "descricao", "categoria")
    @classmethod
    def non_blank(cls, value):
        if not value.strip():
            raise ValueError("O campo não pode ficar vazio.")
        return value.strip()

    @field_validator("imagem_url")
    @classmethod
    def safe_image(cls, value):
        from urllib.parse import urlsplit
        parsed = urlsplit(value)
        if (parsed.scheme == "https" and parsed.netloc and not parsed.username
                and not parsed.password):
            return value
        if re.fullmatch(r"/imagens/[a-zA-Z0-9_/-]+\.(png|jpg|jpeg|webp|svg)", value) and ".." not in value:
            return value
        raise ValueError("Use uma URL HTTPS ou imagem local em /imagens/.")


class ItemPedido(Input):
    id_produto: int = Field(gt=0, strict=True)
    quantidade: int = Field(gt=0, le=1000, strict=True)


class Pedido(Input):
    itens: list[ItemPedido] = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def unique_items(self):
        if len({i.id_produto for i in self.itens}) != len(self.itens):
            raise ValueError("Agrupe as quantidades de cada produto em um único item.")
        return self
