from pydantic import BaseModel, Field
from uuid import uuid4

class Pedido(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user: str
    produto: str
    quantidade: int
    status: str = "PENDENTE"