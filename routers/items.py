from fastapi import APIRouter, Depends, FastAPI, HTTPException
from ..models.models import SessionLocal, Customers, Items, Orders, sa, so
from ..models import schemas as schemas
from datetime import date


router = APIRouter(tags=['items'])

'''
@router.get("/customers/", tags=["users"])
async def read_customers():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/customers/{username}", tags=["users"])
async def read_customer(username: str):
    return {"username": username}
'''

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.Item, db: so.Session = Depends(get_db)):
    db_item = Items(item_id=item.item_id, item_description=item.item_description, item_price=item.item_price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: so.Session = Depends(get_db)):
    return db.query(Items).offset(skip).limit(limit).all()

@router.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: so.Session = Depends(get_db)):
    db_item = db.query(Items).filter(Items.item_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.get("/items/description/")
def get_orders_for_item(sub_desc: str, db: so.Session = Depends(get_db)):
    stmt = sa.select(Orders.order_id,  Items.item_description, Orders.order_qty).join(Items.orders).where(Items.item_description.contains('TV'))
    result = db.execute(stmt).mappings().all()
    return result