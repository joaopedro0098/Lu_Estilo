from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from dependencies.database import get_db
from Models.products_models import Product
from Schemas.product_schemas import ProductCreate, Product as ProductSchema, PaginatedProductResponse, ProductUpdate
from typing import List, Optional
from datetime import date

router = APIRouter()

@router.get("/", response_model=PaginatedProductResponse)
async def read_products(
    db: Session = Depends(get_db),
    price_min: Optional[float] = Query(None, description="Minimum price filter"),
    price_max: Optional[float] = Query(None, description="Maximum price filter"),
    section: Optional[str] = Query(None, description="Filter by section"),
    stock_min: Optional[int] = Query(None, description="Minimum stock filter"),
    stock_max: Optional[int] = Query(None, description="Maximum stock filter"),
    page: int = Query(1, description="Page number", ge=1),
    limit: int = Query(10, description="Items per page", ge=1, le=100)
):
    # Base query
    query = db.query(Product)
    
    # Apply filters
    if price_min is not None:
        query = query.filter(Product.value >= price_min)
    if price_max is not None:
        query = query.filter(Product.value <= price_max)
    if section:
        query = query.filter(Product.section.ilike(f"%{section}%"))
    if stock_min is not None:
        query = query.filter(Product.stock >= stock_min)
    if stock_max is not None:
        query = query.filter(Product.stock <= stock_max)
    
    # Calculate total count before pagination
    total_count = query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    products = query.offset(offset).limit(limit).all()
    
    # Calculate total pages
    total_pages = (total_count + limit - 1) // limit
    
    return PaginatedProductResponse(
        items=products,
        total=total_count,
        page=page,
        limit=limit,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )

# Rota para criar um novo produto
@router.post("/", response_model=ProductSchema)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    # Verifica se já existe um produto com o mesmo nome
    produto_existente = db.query(Product).filter(
        Product.name.ilike(product.name)
    ).first()
    
    if produto_existente:
        raise HTTPException(
            status_code=400,
            detail=f"Já existe um produto cadastrado com o nome '{product.name}'"
        )
    
    # Verifica se já existe um produto com o mesmo código de barras
    barcode_existente = db.query(Product).filter(
        Product.barcode == product.barcode
    ).first()
    
    if barcode_existente:
        raise HTTPException(
            status_code=400,
            detail=f"Já existe um produto cadastrado com o código de barras '{product.barcode}'"
        )
    
    # Cria o novo produto
    novo_produto = Product(
        name=product.name,
        description=product.description,
        value=product.value,
        barcode=product.barcode,
        section=product.section,
        due_date=product.due_date,
        img_url=product.img_url,
        stock=product.stock  # Usa o valor do stock informado
    )
    
    try:
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
        return novo_produto
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar produto: {str(e)}"
        )

# Rota para obter produto específico
@router.get("/{product_id}", response_model=ProductSchema)
async def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    # Busca o produto pelo ID
    product = db.query(Product).filter(Product.id == product_id).first()
    
    # Se não encontrar o produto, retorna 404
    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )
    
    return product

# Rota para atualizar um produto existente
@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    # Busca o produto pelo ID
    product = db.query(Product).filter(Product.id == product_id).first()
    
    # Se não encontrar o produto, retorna 404
    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )
    
    # Verifica se o novo nome já existe (se estiver sendo atualizado)
    if product_update.name:
        existing_product = db.query(Product).filter(
            and_(
                Product.name.ilike(product_update.name),
                Product.id != product_id
            )
        ).first()
        
        if existing_product:
            raise HTTPException(
                status_code=400,
                detail=f"Already exists a product with name '{product_update.name}'"
            )
    
    # Verifica se o novo código de barras já existe (se estiver sendo atualizado)
    if product_update.barcode:
        existing_product = db.query(Product).filter(
            and_(
                Product.barcode == product_update.barcode,
                Product.id != product_id
            )
        ).first()
        
        if existing_product:
            raise HTTPException(
                status_code=400,
                detail=f"Already exists a product with barcode '{product_update.barcode}'"
            )
    
    # Atualiza apenas os campos que foram fornecidos
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    try:
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error updating product: {str(e)}"
        )

# Rota para deletar um produto existente
@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    # Busca o produto pelo ID
    product = db.query(Product).filter(Product.id == product_id).first()
    
    # Se não encontrar o produto, retorna 404
    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )
    
    try:
        # Remove o produto
        db.delete(product)
        db.commit()
        
        return {
            "message": f"Product with ID {product_id} successfully deleted",
            "product_id": product_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting product: {str(e)}"
        )
