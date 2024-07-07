from pydantic import BaseModel
from typing import SupportsComplex
from datetime import date

class ItemBase(BaseModel):
    item_id: str


class ItemForOrder():
    item_id: str

    class Config:
        orm_mode = True


class Item(ItemBase):
    item_description: str
    item_price: SupportsComplex

    class Config:
        orm_mode = True


class CustomerBase(BaseModel):
    cust_id: str
    cust_firstname: str
    cust_lastname: SupportsComplex


class Customer(CustomerBase):

    class Config:
        orm_mode = True



class OrderBase(BaseModel):
    order_id: str
    order_date: date
    order_qty: int
    cust_id: int
    item_id: int


class Order(OrderBase):

    class Config:
        orm_mode = True