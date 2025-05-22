from fastapi import FastAPI
from Routers import (
    auth_routes,
    clients_routes,
    sections_routes, 
    categories_routes,
    products_routes,
    orders_routes, 
    whatsapp_routes
)

app = FastAPI() #Criando uma instancia da classe FastAPI
#para rodar o nosso código, executar no terminal -> uvicorn main:app --reload

app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticação"])
app.include_router(categories_routes.router, prefix="/categorias", tags=["Categorias"])
app.include_router(products_routes.router, prefix="/produtos", tags=["Produtos"])
app.include_router(sections_routes.router, prefix="/secoes", tags=["Seções"])
app.include_router(orders_routes.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(clients_routes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(whatsapp_routes.router, prefix="/whatsapp", tags=["Whatsapp"])

