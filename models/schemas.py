from pydantic import BaseModel
from decimal import Decimal
from datetime import date

class ItemBase(BaseModel):
    item_id: int



class Item(ItemBase):
    item_description: str
    item_price: Decimal

    class Config:
        from_attributes = True



class CustomerBase(BaseModel):
    cust_id: int
    cust_firstname: str
    cust_lastname: str


class Customer(CustomerBase):

    class Config:
        from_attributes = True



class OrderBase(BaseModel):
    order_id: int
    order_date: date
    order_qty: int
    cust_id: int
    item_id: int


class Order(OrderBase):

    class Config:
        from_attributes = True