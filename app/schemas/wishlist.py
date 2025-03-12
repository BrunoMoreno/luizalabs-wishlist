from typing import List
from pydantic import BaseModel, ConfigDict
from app.schemas.product import Product


class WishlistResponse(BaseModel):
    products: List[Product]

    model_config = ConfigDict(from_attributes=True)
