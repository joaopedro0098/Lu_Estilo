from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_orders(): 
    return {"message": "Rota de pedidos"}