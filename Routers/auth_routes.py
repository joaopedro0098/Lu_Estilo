from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
async def register():
    return {"message": "Registro de novo usuário"}

@router.post("/login")
async def login():
    return {"message": "Autenticação de usuário"}

@router.post("/refresh-token")
async def refresh_token():
    return {"message": "Refresh de token JWT"}