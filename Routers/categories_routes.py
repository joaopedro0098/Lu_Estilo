from fastapi import APIRouter

router = APIRouter()

# Definindo as listas de validação como constantes no início do arquivo
CATEGORIAS_VALIDAS = ["tenis", "sapatilhas", "botas", "sapatos-sociais", "chinelos"]
SECOES_VALIDAS = ["feminino", "masculino"]

# Rotas para listar todas as categorias
@router.get("/")
async def read_categories():
    return {
        "message": "Lista de categorias",
        "categorias": CATEGORIAS_VALIDAS
    }

# Rota para listar produtos por categoria
@router.get("/{categoria}")
async def read_products_by_category(categoria: str):
    if categoria.lower() not in CATEGORIAS_VALIDAS:
        return {"error": "Categoria não encontrada"}
    
    return {
        "message": f"Produtos da categoria {categoria}",
        "categoria": categoria
    }

# Rota para listar produtos por categoria e seção
@router.get("/{categoria}/{secao}")
async def read_products_by_category_and_section(categoria: str, secao: str):
    if categoria.lower() not in CATEGORIAS_VALIDAS:
        return {"error": "Categoria não encontrada"}
    
    if secao.lower() not in SECOES_VALIDAS:
        return {"error": "Seção não encontrada"}
    
    return {
        "message": f"Produtos da categoria {categoria} na seção {secao}",
        "categoria": categoria,
        "secao": secao
#aqui o produto "botas" ficaria com a rota Masculinos/Botas/id do produto
    }

# Rota para criar nova categoria (apenas admin)
@router.post("/")
async def create_category():
    return {"message": "Criar nova categoria"}

# Rota para atualizar categoria (apenas admin)
@router.put("/{categoria}")
async def update_category(categoria: str):
    return {"message": f"Atualizar categoria {categoria}"}

# Rota para deletar categoria (apenas admin)
@router.delete("/{categoria}")
async def delete_category(categoria: str):
    return {"message": f"Deletar categoria {categoria}"}