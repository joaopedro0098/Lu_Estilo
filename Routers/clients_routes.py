from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_clients(): 
    return {"message": "Rota de clientes"}