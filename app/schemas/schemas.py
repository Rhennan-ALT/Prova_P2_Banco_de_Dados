from pydantic import BaseModel
from typing import Optional

class Create(BaseModel):
    user: str
    produto: str
    quantidade: int

class PedidoMagic(BaseModel):
    id: str
    user: str
    produto: str
    quantidade: int
    status: str

    class Config:
        from_attributes = True