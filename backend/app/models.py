from sqlalchemy import Column, Integer, Float, String
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    sale_price = Column(Float)
    rating = Column(Float)
    feedback_count = Column(Integer)
    query = Column(String)