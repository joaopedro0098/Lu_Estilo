from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/")
async def read_clients( 
    nome: str = Query(None, description="Filtrar por nome"),
    email: str = Query(None, description="Filtrar por email"),
    pagina: int = Query(1, description="Número da página"),
    limite: int = Query(5, description="Itens por página")

):
    return {
        "message": "Listagem de clientes", 
        "filtros": {
            "nome": nome, 
            "email": email, 
            "pagina": pagina, 
            "limite": limite
        }
    }

# Rota para criar um novo cliente 
@router.post("/")
async def create_client(): 
    return {"message":"Criar novo cliente"}

# Rota para obter cliente específico
@router.get("/{cliente_id}")
async def read_client(cliente_id: int): 
    return {
        "message": f"Detalhes do cliente {cliente_id}",
        "cliente_id": cliente_id
    }

# Rota para atualizar um cliente existente
@router.put("/{cliente_id}")
async def update_client(cliente_id: int): 
    return {
        "message": f"Atualizar cliente {cliente_id}",
        "cliente_id": cliente_id
    }

# Rota para deletar um cliente existente
@router.delete("/{cliente_id}")
async def delete_client(cliente_id: int): 
    return {
        "message": f"Deletar cliente {cliente_id}",
        "cliente_id": cliente_id
    }
