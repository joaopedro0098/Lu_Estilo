from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from dependencies.database import get_db
from Models.categories_models import Category
from pydantic import BaseModel

# Schema para validação dos dados
class CategoryBase(BaseModel):
    name: str
    description: str

router = APIRouter()

# Rotas para listar todas as categorias
@router.get("/")
async def read_categories(db: Session = Depends(get_db)):
    categorias = db.query(Category).all()
    return categorias

# Rota para buscar uma categoria específica
@router.get("/{categoria_id}")
async def read_category(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Category).filter(Category.id == categoria_id).first()
    if not categoria:
        return {"error": "Categoria não encontrada"}
    return categoria

# Rota para criar nova categoria
@router.post("/")
async def create_category(
    category: CategoryBase,
    db: Session = Depends(get_db)
):
    nova_categoria = Category(
        name=category.name,
        description=category.description
    )
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria

# Rota para atualizar categoria
@router.put("/{categoria_id}")
async def update_category(
    categoria_id: int,
    category: CategoryBase,
    db: Session = Depends(get_db)
):
    categoria = db.query(Category).filter(Category.id == categoria_id).first()
    if not categoria:
        return {"error": "Categoria não encontrada"}
    
    categoria.name = category.name
    categoria.description = category.description
    
    db.commit()
    db.refresh(categoria)
    return categoria

# Rota para deletar categoria
@router.delete("/{categoria_id}")
async def delete_category(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    categoria = db.query(Category).filter(Category.id == categoria_id).first()
    if not categoria:
        return {"error": "Categoria não encontrada"}
    
    db.delete(categoria)
    db.commit()
    return {"message": "Categoria deletada com sucesso"}