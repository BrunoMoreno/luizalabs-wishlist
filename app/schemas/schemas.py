from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class CustomerBase(BaseModel):
    name: str
    email: EmailStr

class CustomerCreate(CustomerBase):
    password: str

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    id: str
    title: str
    price: float
    image: Optional[str] = None
    brand: Optional[str] = None
    review_score: Optional[float] = None

class Product(ProductBase):
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class WishlistResponse(BaseModel):
    products: List[Product]

    class Config:
        from_attributes = True 