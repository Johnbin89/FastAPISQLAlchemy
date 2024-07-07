from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response
from ..models.models import SessionLocal, Customers, Items, Orders, sa, so
from ..models import schemas as schemas
from datetime import date


router = APIRouter(tags=['orders'])

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



@router.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: so.Session = Depends(get_db)):
    return db.query(Orders).offset(skip).limit(limit).all()

@router.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: so.Session = Depends(get_db)):
    db_order = db.query(Orders).filter(Orders.order_id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/orders/{order_id}")
def delete_order(order_id: str, db: so.Session = Depends(get_db)):
    order_query = db.query(Orders).filter(Orders.order_id == order_id)
    order = order_query.first()
    if not order:
        raise HTTPException(status_code=404,
                            detail=f'No order with this id: {order_id} found')
    order_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)