from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_categories():
    return {"message": "Rota de categorias"}