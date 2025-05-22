from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_products(): 
    return {"message": "Lista de produtos"}

@router.post("/")
async def create_product():
    return {"message": "Criar produto"}

@router.get("/{product_id}")
async def read_product(product_id: int): 
    return {"message": f"Detalhes do produto {product_id}"}

@router.put("/{product_id}")
async def update_product(product_id: int): 
    return {"message": f"Atualizar produto {product_id}"}

@router.delete("/{product_id}")
async def delete_product(product_id: int):
    return {"message": f"Deletar produto {product_id}"}

