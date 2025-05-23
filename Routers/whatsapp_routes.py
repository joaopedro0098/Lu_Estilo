from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_whatsapp(): 
    return {"message": "Rota de whatsapp"}
