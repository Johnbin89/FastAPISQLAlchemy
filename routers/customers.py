from fastapi import APIRouter, Depends, FastAPI, HTTPException
from ..models.models import SessionLocal, Customers, Items, Orders, sa
from ..models import schemas as schemas
from datetime import date


router = APIRouter()

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


@router.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.Customer, db: sa.Session = Depends(get_db)):
    db_customer = Customers(cust_id=customer.cust_id, cust_firstname=customer.cust_firstname, cust_lastname=customer.cust_lastname)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.get("/customers/", response_model=list[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: sa.Session = Depends(get_db)):
    return db.query(Customers).offset(skip).limit(limit).all()


@router.get("/customers/{customer_id}", response_model=schemas.User)
def read_customer(customer_id: int, db: sa.Session = Depends(get_db)):
    db_customer = db.query(Customers).filter(Customers.cust_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@router.post("/customers/{customer_id}/orders/", response_model=schemas.Order)
def create_order_for_customer(customer_id: int, item: schemas.ItemForOrder, date: date, qty: int, db: sa.Session = Depends(get_db)):
    db_customer = db.query(Customers).filter(Customers.cust_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db_item = db.query(Items).filter(Items.item_id == item.item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_order = Orders(order_date=date, order_qty=qty, cust_id=db_customer.cust_id, item_id=db_item.item_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order



@router.get("/customers/{customer_id}/orders", response_model=list[schemas.Order])
def read_customer_orders(cust_id: int, db: sa.Session = Depends(get_db)):
    db_customer = db.query(Customers).filter(Customers.cust_id == cust_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db_customer_orders = db.query(Orders).filter(Customers.cust_id == db_customer.cust_id).all()
    if db_customer_orders is None:
        raise HTTPException(status_code=404, detail="Customer has not placed orders yet")
    return db_customer_orders

