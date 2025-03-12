from pydantic import BaseModel, EmailStr, ConfigDict


class CustomerBase(BaseModel):
    name: str
    email: EmailStr


class CustomerCreate(CustomerBase):
    password: str


class Customer(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
