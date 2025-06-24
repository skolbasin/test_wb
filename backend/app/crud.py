from sqlalchemy.orm import Session
from . import models, schemas


def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        min_price: float = None,
        max_price: float = None,
        min_rating: float = None,
        min_feedback: int = None,
        query: str = None
):
    query_filter = db.query(models.Product)

    if min_price is not None:
        query_filter = query_filter.filter(models.Product.price >= min_price)
    if max_price is not None:
        query_filter = query_filter.filter(models.Product.price <= max_price)
    if min_rating is not None:
        query_filter = query_filter.filter(models.Product.rating >= min_rating)
    if min_feedback is not None:
        query_filter = query_filter.filter(models.Product.feedback_count >= min_feedback)
    if query is not None:
        query_filter = query_filter.filter(models.Product.query == query)

    return query_filter.offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product