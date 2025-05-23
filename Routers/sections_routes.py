from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_sections(): 
    return {"message": "Rota de seções"}