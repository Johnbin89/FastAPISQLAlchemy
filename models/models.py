import os
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import date
from typing_extensions import Annotated
from decimal import Decimal

basedir = os.path.abspath(os.path.dirname(__file__))
database_url='sqlite:///' + os.path.join(basedir, 'data.sqlite')
engine = sa.create_engine(database_url, connect_args={"check_same_thread": False})
#check_same_thread only for SQLite: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-engine

SessionLocal = so.sessionmaker(bind=engine)

str_30 = Annotated[str, 30]
str_50 = Annotated[str, 50]
num_10_2 = Annotated[Decimal, 10]

#https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapping-multiple-type-configurations-to-python-types
class Base(so.DeclarativeBase):
    registry = so.registry(
        type_annotation_map={
            str_30: sa.String(30),
            str_50: sa.String(50),
            num_10_2: sa.Numeric(10, 2),
        }
    )

class Customers(Base):
    __tablename__ = 'customers'

    cust_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    cust_firstname: so.Mapped[str]
    cust_lastname: so.Mapped[str]

    orders = so.relationship("Orders", back_populates="customer")

class Items(Base):
    __tablename__ = 'items'

    item_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    item_description: so.Mapped[str]
    item_price: so.Mapped[num_10_2] = so.mapped_column(nullable=True)

    orders = so.relationship("Orders", back_populates="item")

class Orders(Base):
    __tablename__ = 'orders'

    order_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    order_date: so.Mapped[date]
    order_qty: so.Mapped[int]
    cust_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("customers.cust_id"))
    item_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("items.item_id"))

    customer = so.relationship("Customers", back_populates="orders")
    item = so.relationship("Items", back_populates="orders")

#reliationships backpopulate
#https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-relationships


