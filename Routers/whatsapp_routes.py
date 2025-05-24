from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.database import get_db

router = APIRouter()

@router.get("/")
async def read_whatsapp(db: Session = Depends(get_db)): 
    return {"message": "Rota de whatsapp"}
