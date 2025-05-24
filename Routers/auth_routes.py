from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.database import get_db

router = APIRouter()

@router.post("/register")
async def register(db: Session = Depends(get_db)):
    return {"message": "Registro de novo usuário"}

@router.post("/login")
async def login(db: Session = Depends(get_db)):
    return {"message": "Autenticação de usuário"}

@router.post("/refresh-token")
async def refresh_token(db: Session = Depends(get_db)):
    return {"message": "Refresh de token JWT"}