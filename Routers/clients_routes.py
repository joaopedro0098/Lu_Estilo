from fastapi import APIRouter, Query, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from dependencies.database import get_db
from Models.clients_models import Client
from Models.orders_models import Order
from Schemas.client_schemas import (
    ClientCreate, 
    Client as ClientSchema,
    PaginatedClientResponse,
    ClientUpdate
)
from typing import List

router = APIRouter()

@router.get("/", response_model=PaginatedClientResponse)
async def read_clients( 
    db: Session = Depends(get_db),
    nome: str = Query(None, description="Filtrar por nome"),
    email: str = Query(None, description="Filtrar por email"),
    cpf: str = Query(None, description="Filtrar por CPF"),
    pagina: int = Query(1, description="Número da página"),
    limite: int = Query(5, description="Itens por página")
):
    # Calcula o offset para paginação
    offset = (pagina - 1) * limite
    
    # Query base
    query = db.query(Client)
    
    # Aplica filtros se fornecidos
    if nome:
        query = query.filter(Client.name.ilike(f"%{nome}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))
    if cpf:
        query = query.filter(Client.cpf.ilike(f"%{cpf}%"))
    
    # Aplica paginação
    total = query.count()
    clientes = query.offset(offset).limit(limite).all()
    
    return PaginatedClientResponse(
        total=total,
        pagina=pagina,
        limite=limite,
        clientes=clientes
    )

@router.post("/", response_model=ClientSchema)
async def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    # Verifica se já existe um cliente com o mesmo CPF
    if client.cpf:
        cliente_existente = db.query(Client).filter(Client.cpf == client.cpf).first()
        if cliente_existente:
            raise HTTPException(
                status_code=400,
                detail="Já existe um cliente cadastrado com este CPF"
            )
    
    # Verifica se já existe um cliente com o mesmo email
    cliente_existente = db.query(Client).filter(Client.email == client.email).first()
    if cliente_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe um cliente cadastrado com este email"
        )
    
    novo_cliente = Client(
        name=client.name,
        email=client.email,
        phone=client.phone,
        address=client.address,
        cpf=client.cpf
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

@router.get("/{cliente_id}", response_model=ClientSchema)
async def read_client(cliente_id: int, db: Session = Depends(get_db)): 
    cliente = db.query(Client).filter(Client.id == cliente_id).first()
    
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    return cliente

@router.put("/{cliente_id}", response_model=ClientSchema)
async def update_client(
    cliente_id: int, 
    cliente_update: ClientUpdate,
    db: Session = Depends(get_db)
): 
    cliente = db.query(Client).filter(Client.id == cliente_id).first()
    
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    # Verifica se o novo CPF já existe em outro cliente
    if cliente_update.cpf and cliente_update.cpf != cliente.cpf:
        cpf_existente = db.query(Client).filter(
            Client.cpf == cliente_update.cpf,
            Client.id != cliente_id
        ).first()
        if cpf_existente:
            raise HTTPException(
                status_code=400,
                detail="Já existe outro cliente cadastrado com este CPF"
            )
    
    # Verifica se o novo email já existe em outro cliente
    if cliente_update.email and cliente_update.email != cliente.email:
        email_existente = db.query(Client).filter(
            Client.email == cliente_update.email,
            Client.id != cliente_id
        ).first()
        if email_existente:
            raise HTTPException(
                status_code=400,
                detail="Já existe outro cliente cadastrado com este email"
            )
    
    # Atualiza apenas os campos fornecidos
    update_data = cliente_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cliente, field, value)
    
    db.commit()
    db.refresh(cliente)
    
    return cliente

@router.delete("/{cliente_id}", response_model=dict)
async def delete_client(cliente_id: int, db: Session = Depends(get_db)): 
    cliente = db.query(Client).filter(Client.id == cliente_id).first()
    
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    pedidos = db.query(Order).filter(Order.client_id == cliente_id).first()
    if pedidos:
        raise HTTPException(
            status_code=400,
            detail=f"Não é possível excluir o cliente {cliente_id} pois existem pedidos associados a ele"
        )
    
    db.delete(cliente)
    db.commit()
    
    return {
        "message": f"Cliente {cliente_id} removido com sucesso",
        "cliente_id": cliente_id
    }
