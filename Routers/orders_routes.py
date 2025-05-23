from fastapi import APIRouter, Query
from datetime import date

router = APIRouter()

@router.get("/")
async def read_orders(
    periodo_inicio: date = Query(None, description="Início do período"),
    periodo_fim: date = Query(None, description="Fim do período"),
    secao: str = Query(None, description="Seção dos produtos"),
    id_pedido: int = Query(None, description="ID do pedido"),
    status: str = Query(None, description="Status do pedido"),
    cliente: int = Query(None, description="ID do cliente")
):
    return {
        "message": "Listagem de pedidos",
        "filtros": {
            "periodo_inicio": periodo_inicio,
            "periodo_fim": periodo_fim,
            "secao": secao,
            "id_pedido": id_pedido,
            "status": status,
            "cliente": cliente
        }
    }

# Rota para criar um novo pedido
@router.post("/")
async def create_order():
    return {"message": "Criar novo pedido"}

# Rota para obter pedido específico
@router.get("/{pedido_id}")
async def read_order(pedido_id: int):
    return {
        "message": f"Detalhes do pedido {pedido_id}",
        "pedido_id": pedido_id
    }

# Rota para atualizar um pedido existente
@router.put("/{pedido_id}")
async def update_order(pedido_id: int):
    return {
        "message": f"Atualizar pedido {pedido_id}",
        "pedido_id": pedido_id
    }

# Rota para deletar um pedido existente
@router.delete("/{pedido_id}")
async def delete_order(pedido_id: int):
    return {
        "message": f"Deletar pedido {pedido_id}",
        "pedido_id": pedido_id
    }