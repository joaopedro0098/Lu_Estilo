from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Date, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .auth_models import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    value = Column(Float, nullable=False)
    barcode = Column(String, unique=True)
    section = Column(String)
    due_date = Column(Date, nullable=True)
    img_url = Column(String)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    orders = relationship("Order", secondary="order_products", back_populates="products")