from fastapi import FastAPI
from Routers import (
    auth_routes,
    clients_routes,
    products_routes,
    orders_routes, 
)

app = FastAPI() #Criando uma instancia da classe FastAPI
#para rodar o nosso código, executar no terminal -> uvicorn main:app --reload

app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticação"])
app.include_router(products_routes.router, prefix="/produtos", tags=["Produtos"])
app.include_router(orders_routes.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(clients_routes.router, prefix="/clientes", tags=["Clientes"])


