# schemas/category_schemas.py
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True