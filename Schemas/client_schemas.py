from pydantic import BaseModel, EmailStr
from typing import List

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str | None = None
    cpf: str | None = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    cpf: str | None = None

class Client(ClientBase):
    id: int

    class Config:
        from_attributes = True

# Novo schema para resposta paginada
class PaginatedClientResponse(BaseModel):
    total: int
    pagina: int
    limite: int
    clientes: List[Client]

    class Config:
        from_attributes = True