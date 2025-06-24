from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from .parsers import wildberries
from typing import Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/parse/")
def parse_products(query: str, db: Session = Depends(get_db)):
    products_data = wildberries.parse_wildberries(query)
    for product_data in products_data:
        crud.create_product(db=db, product=product_data)
    return {"status": "success", "parsed_items": len(products_data)}

@app.get("/api/products/", response_model=list[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    min_feedback: Optional[int] = None,
    query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    products = crud.get_products(
        db,
        skip=skip,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        min_feedback=min_feedback,
        query=query
    )
    return products