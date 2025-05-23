from fastapi import APIRouter, Query

router = APIRouter()

# Definindo as seções válidas como constantes
SECOES_VALIDAS = ["masculino", "feminino"]

@router.get("/")
async def read_sections(
    pagina: int = Query(1, description="Número da página"),
    limite: int = Query(10, description="Itens por página")
):
    return {
        "message": "Listagem de seções",
        "secoes": SECOES_VALIDAS,
        "filtros": {
            "pagina": pagina,
            "limite": limite
        }
    }

# Rota para listar produtos por seção
@router.get("/{secao}")
async def read_products_by_section(
    secao: str,
    categoria: str = Query(None, description="Filtrar por categoria"),
    preco: float = Query(None, description="Filtrar por preço"),
    disponivel: bool = Query(None, description="Filtrar por disponibilidade"),
    pagina: int = Query(1, description="Número da página"),
    limite: int = Query(10, description="Itens por página")
):
    if secao.lower() not in SECOES_VALIDAS:
        return {"error": "Seção não encontrada"}
    
    return {
        "message": f"Produtos da seção {secao}",
        "secao": secao,
        "filtros": {
            "categoria": categoria,
            "preco": preco,
            "disponivel": disponivel,
            "pagina": pagina,
            "limite": limite
        }
    }

# Rota para criar nova seção (apenas admin)
@router.post("/")
async def create_section():
    return {"message": "Criar nova seção"}

# Rota para atualizar seção (apenas admin)
@router.put("/{secao}")
async def update_section(secao: str):
    if secao.lower() not in SECOES_VALIDAS:
        return {"error": "Seção não encontrada"}
    return {"message": f"Atualizar seção {secao}"}

# Rota para deletar seção (apenas admin)
@router.delete("/{secao}")
async def delete_section(secao: str):
    if secao.lower() not in SECOES_VALIDAS:
        return {"error": "Seção não encontrada"}
    return {"message": f"Deletar seção {secao}"}