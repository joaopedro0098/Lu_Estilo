from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    description: str
    value: float
    barcode: str
    section: str
    due_date: Optional[date] = None
    img_url: str

class ProductCreate(ProductBase):
    stock: int = Field(default=0, ge=0, description="Initial stock quantity")

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    value: float | None = None
    barcode: str | None = None
    section: str | None = None
    due_date: date | None = None
    img_url: str | None = None
    stock: int | None = Field(None, ge=0, description="Stock quantity")

class Product(ProductBase):
    id: int
    stock: int

    class Config:
        from_attributes = True

class PaginatedProductResponse(BaseModel):
    items: List[Product]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool

    class Config:
        from_attributes = True