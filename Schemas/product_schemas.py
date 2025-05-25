from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category_id: int | None = None

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True