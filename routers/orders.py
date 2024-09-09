from fastapi import APIRouter, Depends, HTTPException, status
from fastapisqlalchemy.models.models import get_db, AsyncSession, Orders, sa
from fastapisqlalchemy.models import schemas as schemas

router = APIRouter(tags=['orders'])

'''
@router.get("/customers/", tags=["users"])
async def read_customers():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/customers/{username}", tags=["users"])
async def read_customer(username: str):
    return {"username": username}
'''


@router.get("/orders/", response_model=list[schemas.Order])
async def read_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        stmt = sa.select(Orders).offset(skip).limit(limit)
        orders = (await db.execute(stmt)).scalars().fetchall()
    return orders

@router.get("/orders/{order_id}", response_model=schemas.Order)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        stmt = sa.select(Orders).filter(Orders.order_id == order_id)
        try:
           db_order = (await db.execute(stmt)).scalar_one()
           return db_order
        except sa.exc.NoResultFound:
            raise HTTPException(status_code=404, detail="Order not found")

@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        stmt = sa.select(Orders).where(Orders.order_id == order_id)
        try:
            order = (await db.execute(stmt)).scalar_one()
        except sa.exc.NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No order with id: {order_id} found')
        await db.delete(order)