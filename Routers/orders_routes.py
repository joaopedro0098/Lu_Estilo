from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, insert
from dependencies.database import get_db
from datetime import date, datetime
from Models.orders_models import Order, OrderStatus, order_products
from Models.products_models import Product
from Models.clients_models import Client
from Schemas.order_schemas import OrderCreate, Order as OrderSchema, PaginatedOrderResponse, OrderUpdate
from typing import List, Optional

router = APIRouter()

STATUS_VALIDOS = ["pendente", "confirmado", "em_preparo", "pronto", "entregue", "cancelado"]


@router.get("/", response_model=PaginatedOrderResponse)
async def read_orders(
    db: Session = Depends(get_db),
    start_date: Optional[date] = Query(None, description="Start date of the period"),
    end_date: Optional[date] = Query(None, description="End date of the period"),
    order_id: Optional[int] = Query(None, description="Order ID"),
    status: Optional[str] = Query(None, description="Order status"),
    client_id: Optional[int] = Query(None, description="Client ID"),
    product_section: Optional[str] = Query(None, description="Product section"),
    page: int = Query(1, description="Page number", ge=1),
    limit: int = Query(10, description="Items per page", ge=1, le=100)
):
    # Base query
    query = db.query(Order)
    
    # Apply filters
    if order_id:
        query = query.filter(Order.id == order_id)
    
    if client_id:
        query = query.filter(Order.client_id == client_id)
    
    if status:
        try:
            status_enum = OrderStatus(status.lower())
            query = query.filter(Order.status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Valid statuses are: {[s.value for s in OrderStatus]}"
            )
    
    if start_date:
        # Convert date to datetime at start of day
        start_datetime = datetime.combine(start_date, datetime.min.time())
        query = query.filter(Order.created_at >= start_datetime)
    
    if end_date:
        # Convert date to datetime at end of day
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(Order.created_at <= end_datetime)
    
    # Filter by product section if specified
    if product_section:
        query = query.join(Order.products).filter(
            Product.section.ilike(f"%{product_section}%")
        )
    
    # Order by creation date (most recent first)
    query = query.order_by(Order.created_at.desc())
    
    # Calculate total count before pagination
    total_count = query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    orders = query.offset(offset).limit(limit).all()
    
    # Calculate total pages
    total_pages = (total_count + limit - 1) // limit
    
    # Formata os pedidos com seus produtos
    formatted_orders = []
    for order in orders:
        # Busca o cliente
        client = db.query(Client).filter(Client.id == order.client_id).first()
        
        # Busca os produtos do pedido com suas quantidades
        order_products_query = db.query(
            Product,
            order_products.c.quantity
        ).join(
            order_products,
            Product.id == order_products.c.product_id
        ).filter(
            order_products.c.order_id == order.id
        ).all()
        
        # Constrói a lista de produtos para a resposta
        products_response = []
        for product, quantity in order_products_query:
            products_response.append({
                "product_id": product.id,
                "product_name": product.name,
                "quantity": quantity,
                "value": product.value,
                "section": product.section
            })
        
        # Cria o objeto de pedido formatado
        formatted_order = {
            "id": order.id,
            "client_id": order.client_id,
            "client_name": client.name if client else None,
            "status": order.status.value,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "products": products_response
        }
        formatted_orders.append(formatted_order)
    
    return PaginatedOrderResponse(
        items=formatted_orders,
        total=total_count,
        page=page,
        limit=limit,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )

# Rota para criar um novo pedido
@router.post("/", response_model=OrderSchema)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    try:
        # Verifica se o cliente existe pelo nome
        client = db.query(Client).filter(Client.name.ilike(f"%{order.client_name}%")).first()
        if not client:
            raise HTTPException(
                status_code=404,
                detail=f"Cliente com nome '{order.client_name}' não encontrado"
            )
        
        # Cria o pedido
        new_order = Order(
            client_id=client.id,
            status=OrderStatus.PENDING,
            total_amount=0.0  # Será calculado após adicionar os itens
        )
        db.add(new_order)
        db.flush()  # Para obter o ID do pedido
        
        total_amount = 0.0
        products_to_add = []
        
        # Adiciona os itens do pedido
        for item in order.products:
            # Verifica se o produto existe pelo nome
            product = db.query(Product).filter(Product.name.ilike(f"%{item.product_name}%")).first()
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Produto com nome '{item.product_name}' não encontrado"
                )
            
            # Verifica se há estoque suficiente
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estoque insuficiente para o produto '{product.name}'. Disponível: {product.stock}"
                )
            
            # Atualiza o estoque do produto
            product.stock -= item.quantity
            
            # Atualiza o total do pedido
            item_total = product.value * item.quantity
            total_amount += item_total
            
            # Adiciona os dados na tabela de associação
            stmt = insert(order_products).values(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.value,
                created_at=datetime.now()
            )
            db.execute(stmt)
            
            # Adiciona o produto à lista de produtos do pedido
            products_to_add.append(product)
        
        # Atualiza o total do pedido
        new_order.total_amount = total_amount
        
        # Adiciona os produtos ao pedido
        new_order.products = products_to_add
        
        # Commit das alterações
        db.commit()
        db.refresh(new_order)
        
        # Busca os produtos do pedido com suas quantidades
        order_products_query = db.query(
            Product,
            order_products.c.quantity
        ).join(
            order_products,
            Product.id == order_products.c.product_id
        ).filter(
            order_products.c.order_id == new_order.id
        ).all()
        
        # Constrói a lista de produtos para a resposta
        products_response = []
        for product, quantity in order_products_query:
            products_response.append({
                "product_id": product.id,
                "product_name": product.name,
                "quantity": quantity,
                "value": product.value,
                "section": product.section
            })
        
        # Cria o objeto de resposta
        response = {
            "id": new_order.id,
            "client_id": new_order.client_id,
            "client_name": client.name,
            "status": new_order.status.value,
            "total_amount": new_order.total_amount,
            "created_at": new_order.created_at,
            "products": products_response
        }
        
        return response
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar pedido: {str(e)}"
        )


# Rota para obter pedido específico
@router.get("/{pedido_id}", response_model=OrderSchema)
async def read_order(pedido_id: int, db: Session = Depends(get_db)):
    # Busca o pedido pelo ID
    order = db.query(Order).filter(Order.id == pedido_id).first()
    
    # Se não encontrar o pedido, retorna 404
    if not order:
        raise HTTPException(
            status_code=404,
            detail=f"Order with ID {pedido_id} not found"
        )
    
    # Busca o cliente
    client = db.query(Client).filter(Client.id == order.client_id).first()
    
    # Busca os produtos do pedido com suas quantidades
    order_products_query = db.query(
        Product,
        order_products.c.quantity
    ).join(
        order_products,
        Product.id == order_products.c.product_id
    ).filter(
        order_products.c.order_id == order.id
    ).all()
    
    # Constrói a lista de produtos para a resposta
    products_response = []
    for product, quantity in order_products_query:
        products_response.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": quantity,
            "value": product.value,
            "section": product.section
        })
    
    # Cria o objeto de resposta
    response = {
        "id": order.id,
        "client_id": order.client_id,
        "client_name": client.name if client else None,
        "status": order.status.value,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "products": products_response
    }
    
    return response

# Rota para atualizar um pedido existente
@router.put("/{pedido_id}", response_model=OrderSchema)
async def update_order(
    pedido_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db)
):
    # Busca o pedido pelo ID
    order = db.query(Order).filter(Order.id == pedido_id).first()
    
    # Se não encontrar o pedido, retorna 404
    if not order:
        raise HTTPException(
            status_code=404,
            detail=f"Pedido com ID {pedido_id} não encontrado"
        )
    
    try:
        # Atualiza o cliente se fornecido
        if order_update.client_name is not None:
            client = db.query(Client).filter(Client.name.ilike(f"%{order_update.client_name}%")).first()
            if not client:
                raise HTTPException(
                    status_code=404,
                    detail=f"Cliente com nome '{order_update.client_name}' não encontrado"
                )
            order.client_id = client.id
        
        # Atualiza o status se fornecido
        if order_update.status is not None:
            try:
                status_enum = OrderStatus(order_update.status.lower())
                order.status = status_enum
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Status inválido. Status válidos são: {[s.value for s in OrderStatus]}"
                )
        
        # Atualiza os produtos se fornecidos
        if order_update.products is not None:
            # Remove os produtos antigos
            db.execute(order_products.delete().where(order_products.c.order_id == order.id))
            
            total_amount = 0.0
            produtos_nao_encontrados = []
            
            # Adiciona os novos produtos
            for item in order_update.products:
                # Verifica se o produto existe pelo nome (busca mais flexível)
                product = db.query(Product).filter(
                    Product.name.ilike(f"%{item.product_name}%")
                ).first()
                
                if not product:
                    produtos_nao_encontrados.append(item.product_name)
                    continue
                
                # Verifica se há estoque suficiente
                if product.stock < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Estoque insuficiente para o produto '{product.name}'. Disponível: {product.stock}"
                    )
                
                # Atualiza o estoque do produto
                product.stock -= item.quantity
                
                # Atualiza o total do pedido
                total_amount += product.value * item.quantity
                
                # Adiciona os dados na tabela de associação
                stmt = insert(order_products).values(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    unit_price=product.value,
                    created_at=datetime.now()
                )
                db.execute(stmt)
            
            # Se houver produtos não encontrados, retorna erro
            if produtos_nao_encontrados:
                raise HTTPException(
                    status_code=404,
                    detail=f"Os seguintes produtos não foram encontrados: {', '.join(produtos_nao_encontrados)}"
                )
            
            # Atualiza o total do pedido
            order.total_amount = total_amount
        
        # Salva as alterações
        db.commit()
        db.refresh(order)
        
        # Busca o cliente atualizado
        client = db.query(Client).filter(Client.id == order.client_id).first()
        
        # Busca os produtos do pedido com suas quantidades
        order_products_query = db.query(
            Product,
            order_products.c.quantity
        ).join(
            order_products,
            Product.id == order_products.c.product_id
        ).filter(
            order_products.c.order_id == order.id
        ).all()
        
        # Constrói a lista de produtos para a resposta
        products_response = []
        for product, quantity in order_products_query:
            products_response.append({
                "product_id": product.id,
                "product_name": product.name,
                "quantity": quantity,
                "value": product.value,
                "section": product.section
            })
        
        # Cria o objeto de resposta
        response = {
            "id": order.id,
            "client_id": order.client_id,
            "client_name": client.name if client else None,
            "status": order.status.value,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "products": products_response
        }
        
        return response
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar pedido: {str(e)}"
        )

# Rota para deletar um pedido existente
@router.delete("/{pedido_id}")
async def delete_order(pedido_id: int, db: Session = Depends(get_db)):
    try:
        # Busca o pedido pelo ID
        order = db.query(Order).filter(Order.id == pedido_id).first()
        
        # Se não encontrar o pedido, retorna 404
        if not order:
            raise HTTPException(
                status_code=404,
                detail=f"Pedido com ID {pedido_id} não encontrado"
            )
        
        # Busca os produtos do pedido com suas quantidades
        order_products_query = db.query(
            Product,
            order_products.c.quantity
        ).join(
            order_products,
            Product.id == order_products.c.product_id
        ).filter(
            order_products.c.order_id == order.id
        ).all()
        
        # Restaura o estoque dos produtos
        for product, quantity in order_products_query:
            product.stock += quantity
        
        # Remove os produtos do pedido
        db.execute(order_products.delete().where(order_products.c.order_id == order.id))
        
        # Remove o pedido
        db.delete(order)
        
        # Salva as alterações
        db.commit()
        
        return {
            "message": f"Pedido {pedido_id} removido com sucesso",
            "pedido_id": pedido_id,
            "produtos_restaurados": [
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "quantidade_restaurada": quantity
                }
                for product, quantity in order_products_query
            ]
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar pedido: {str(e)}"
        )