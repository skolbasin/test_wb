from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float
    sale_price: float
    rating: float
    feedback_count: int
    query: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True