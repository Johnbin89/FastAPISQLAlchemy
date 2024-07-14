from models.models import SessionLocal, Customers, Orders, Items
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import Row


def dump():
    with SessionLocal() as session:
        with open('items_file', 'wb') as file_handler:
            file_handler.write(dumps(session.query(Items).all()))
        with open('orders_file', 'wb') as file_handler:
            file_handler.write(dumps(session.query(Orders).all()))
        with open('customers_file', 'wb') as file_handler:
            file_handler.write(dumps(session.query(Customers).all()))














def load():
    with SessionLocal() as session:
        with open('items_file', 'rb') as file_handler:
            for row in loads(file_handler.read()):
                if isinstance(row, Row):
                    row = Items(**row._asdict())
                    session.merge(row)
        with open('orders_file', 'rb') as file_handler:
            for row in loads(file_handler.read()):
                if isinstance(row, Row):
                    row = Orders(**row._asdict())
                    session.merge(row)
        with open('customers_file', 'rb') as file_handler:
            for row in loads(file_handler.read()):
                if isinstance(row, Row):
                    row = Customers(**row._asdict())
                    session.merge(row)
        session.commit()











#dump()
load()