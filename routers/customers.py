from fastapi import APIRouter, Depends, HTTPException, status
from ..models.models import get_db, Customers, Items, Orders, sa, AsyncSession
from ..models import schemas as schemas
from datetime import date


router = APIRouter(tags=['customers'])

'''
@router.get("/customers/", tags=["users"])
async def read_customers():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/customers/{username}", tags=["users"])
async def read_customer(username: str):
    return {"username": username}
'''


@router.post("/customers/", response_model=schemas.Customer)
async def create_customer(customer: schemas.Customer, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        stmt = sa.insert(Customers).values({Customers.cust_id :customer.cust_id, 
                                         Customers.cust_firstname :customer.cust_firstname,
                                         Customers.cust_lastname: customer.cust_lastname})\
                .returning(Customers)
        db_customer = (await db.execute(stmt)).scalar_one_or_none()
    return db_customer


@router.get("/customers/", response_model=list[schemas.Customer])
async def read_customers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        stmt = sa.select(Customers).offset(skip).limit(limit)
        customers = await db.execute(stmt)
    return customers.scalars().all()


@router.get("/customers/{customer_id}", response_model=schemas.Customer)
async def read_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        stmt = sa.select(Customers).filter(Customers.cust_id == customer_id)
        db_customer = (await db.execute(stmt)).scalar()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/customers/{customer_id}", response_model=schemas.Customer)
async def edit_customer(customer_id: int, first_name:str = None, last_name :str =None, db: AsyncSession = Depends(get_db)):
    if not any((first_name, last_name)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='You should provide first_name or last_name query params')
    async with db.begin():
        stmt = sa.select(Customers).filter(Customers.cust_id == customer_id)
        try:
            (await db.execute(stmt)).one()
        except sa.exc.NoResultFound:
            raise HTTPException(status_code=404, detail="Customer not found")
    if first_name and last_name:
        new_values_dict = {'cust_firstname': first_name,
                           'cust_lastname': last_name}
    elif first_name:
        new_values_dict = {'cust_firstname': first_name}
    elif last_name:
        new_values_dict = {'cust_lastname': last_name}
    async with db.begin():
        stmt = sa.update(Customers).where(Customers.cust_id == customer_id).values(new_values_dict).returning(Customers)
        db_customer = (await db.execute(stmt)).scalar_one_or_none()
        await db.commit()
    return db_customer


@router.post("/customers/{customer_id}/orders/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
async def create_order_for_customer(customer_id: int, item_id: str, date: date, qty: int, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        stmt = sa.select(Customers).filter(Customers.cust_id == customer_id)
        try:
           (await db.execute(stmt)).one()
        except sa.exc.NoResultFound:
            raise HTTPException(status_code=404, detail="Customer not found")
    
    async with db.begin():
        stmt = sa.select(Items).filter(Items.item_id == item_id)
        try:
           (await db.execute(stmt)).one()
        except sa.exc.NoResultFound:
            raise HTTPException(status_code=404, detail="Item not found")
 
        
    async with db.begin():
        stmt = sa.insert(Orders).values({Orders.order_date :date, 
                                         Orders.order_qty :qty,
                                         Orders.cust_id: customer_id,
                                         Orders.item_id: item_id}).returning(Orders)
        db_order = (await db.execute(stmt)).scalar_one_or_none()
        await db.commit()
    return db_order


#4.1
@router.get("/customers/{customer_id}/orders", response_model=list[schemas.Order])
async def read_customer_orders(customer_id: int, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        stmt = sa.select(Customers).filter(Customers.cust_id == customer_id)
        try:
            (await db.execute(stmt)).one()
        except sa.exc.NoResultFound:
            raise HTTPException(status_code=404, detail="Customer not found")
        
    async with db.begin():
        stmt = sa.select(Orders).filter(Orders.cust_id == customer_id)
        db_customer_orders = (await db.execute(stmt)).scalars().fetchall()
               
    if not  db_customer_orders:
        raise HTTPException(status_code=404, detail="Customer has not placed orders yet")
    return db_customer_orders

#4.2
@router.get("/customers/orders/name")
async def read_customer_orders_by_name(fname: str | None = None, lname: str | None = None, db: AsyncSession = Depends(get_db)):
    '''
    For each order placed by the customer with last_name  or first_name (case insensitive - ilike),
    find the order id, the quantity ordered and the price of the items he has ordered.
    '''
    if fname is None and lname is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide First name or Last name at least")
    if fname and lname:
        stmt = sa.select(Orders.order_id, Orders.order_qty, Items.item_price)\
            .join(Items.orders).join(Orders.customer)\
            .where(Customers.cust_firstname.ilike(fname),
                   Customers.cust_lastname.ilike(lname))
    elif fname:
        stmt = sa.select(Orders.order_id, Orders.order_qty, Items.item_price)\
            .join(Items.orders).join(Orders.customer)\
            .where(Customers.cust_firstname.ilike(fname))
    else:
        stmt = sa.select(Orders.order_id, Orders.order_qty, Items.item_price)\
            .join(Items.orders).join(Orders.customer)\
            .where(Customers.cust_lastname.ilike(lname))
    async with db.begin(): 
        result = await db.execute(stmt)
    return result.mappings().all()   