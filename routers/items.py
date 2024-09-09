from fastapi import APIRouter, Depends, HTTPException
from ..models.models import get_db, AsyncSession, Items, Orders, sa, so
from ..models import schemas as schemas


router = APIRouter(tags=['items'])

'''
@router.get("/customers/", tags=["users"])
async def read_customers():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/customers/{username}", tags=["users"])
async def read_customer(username: str):
    return {"username": username}
'''



@router.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.Item, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        stmt = sa.insert(Items).values({Items.item_id :item.item_id, 
                                         Items.item_description :item.item_description,
                                         Items.item_price: item.item_price})\
                .returning(Items)
        db_item = (await db.execute(stmt)).scalar_one_or_none()
    return db_item


@router.get("/items/", response_model=list[schemas.Item])
async def read_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        stmt = sa.select(Items).offset(skip).limit(limit)
        items = (await db.execute(stmt)).scalars().fetchall()
    return items

@router.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: str, db: so.Session = Depends(get_db)):
    async with db.begin():
        stmt = sa.select(Items).filter(Items.item_id == item_id)
        db_item = (await db.execute(stmt)).scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.get("/items/description/")
async def get_orders_for_item_with_description(sub_desc: str, db: AsyncSession = Depends(get_db)):
    '''
    For the items that include in their description the substring {sub_desc}, find the order id,
    the item description and the quantity at which they have been ordered.
    '''
    async with db.begin():
        stmt = sa.select(Orders.order_id,  Items.item_description, Orders.order_qty)\
            .join(Items.orders).where(Items.item_description.icontains(sub_desc))
        result = await db.execute(stmt)
    return result.mappings().all()