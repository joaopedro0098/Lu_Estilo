from pydantic import BaseModel
from typing import List

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderBase(BaseModel):
    client_id: int
    items: List[OrderItemBase]

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    client_id: int | None = None
    status: str | None = None

class Order(OrderBase):
    id: int
    status: str

    class Config:
        from_attributes = True