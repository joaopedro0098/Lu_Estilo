from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .auth_models import Base

class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# Tabela de associação entre Order e Product
order_products = Table(
    'order_products',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('quantity', Integer, nullable=False),
    Column('unit_price', Float, nullable=False),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    client = relationship("Client", back_populates="orders")
    products = relationship("Product", secondary=order_products, back_populates="orders")

__all__ = ['Order', 'OrderStatus', 'order_products']