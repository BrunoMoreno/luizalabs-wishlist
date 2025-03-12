from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    id: str
    title: str
    price: float
    image: str | None = None
    brand: str
    review_score: float | None = None

    model_config = ConfigDict(from_attributes=True) 