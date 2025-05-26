from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderProductBase(BaseModel):
    product_id: int
    quantity: int

class OrderProduct(OrderProductBase):
    name: str
    value: float
    section: str

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    client_id: int
    products: List[OrderProductBase]

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    client_id: int | None = None
    status: str | None = None

class Order(OrderBase):
    id: int
    status: str
    total_amount: float
    created_at: datetime
    products: List[OrderProduct]

    class Config:
        from_attributes = True

class PaginatedOrderResponse(BaseModel):
    items: List[Order]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool

    class Config:
        from_attributes = True