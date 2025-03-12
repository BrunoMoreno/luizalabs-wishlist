from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.database import Base

# Association table for the many-to-many relationship between customers and products
wishlist_items = Table(
    'wishlist_items',
    Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id', ondelete='CASCADE'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
)

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    products = relationship("Product", secondary=wishlist_items, back_populates="customers", cascade="all, delete")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    price = Column(Float)
    image = Column(String, nullable=True)
    brand = Column(String)
    review_score = Column(Float, nullable=True)
    customers = relationship("Customer", secondary=wishlist_items, back_populates="products", cascade="all, delete") 