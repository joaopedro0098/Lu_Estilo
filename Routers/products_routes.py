from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from dependencies.database import get_db

router = APIRouter()

@router.get("/")
async def read_products(
    db: Session = Depends(get_db),
    categoria: str = Query(None, description="Filtrar por categoria"),
    preco: float = Query(None, description="Filtrar por preço"),
    disponivel: bool = Query(None, description="Filtrar por disponibilidade"),
    pagina: int = Query(1, description="Número da página"),
    limite: int = Query(10, description="Itens por página")
):
    return {
        "message": "Listagem de produtos",
        "filtros": {
            "categoria": categoria,
            "preco": preco,
            "disponivel": disponivel,
            "pagina": pagina,
            "limite": limite
        }
    }

# Rota para criar um novo produto
@router.post("/")
async def create_product(db: Session = Depends(get_db)):
    return {"message": "Criar novo produto"}

# Rota para obter produto específico
@router.get("/{produto_id}")
async def read_product(produto_id: int, db: Session = Depends(get_db)):
    return {
        "message": f"Detalhes do produto {produto_id}",
        "produto_id": produto_id
    }

# Rota para atualizar um produto existente
@router.put("/{produto_id}")
async def update_product(produto_id: int, db: Session = Depends(get_db)):
    return {
        "message": f"Atualizar produto {produto_id}",
        "produto_id": produto_id
    }

# Rota para deletar um produto existente
@router.delete("/{produto_id}")
async def delete_product(produto_id: int, db: Session = Depends(get_db)):
    return {
        "message": f"Deletar produto {produto_id}",
        "produto_id": produto_id
    }
