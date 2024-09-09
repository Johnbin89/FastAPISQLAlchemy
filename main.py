from fastapi import FastAPI
from fastapisqlalchemy.models import models as models
from fastapisqlalchemy.routers import items, customers, orders

#DB migrate:
#makemigrations command: alembic revision --autogenerate -m "<message>"
#upgrade: alembic upgrade head

app = FastAPI()


app.include_router(customers.router)
app.include_router(items.router)
app.include_router(orders.router)
'''
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
'''

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!",
            "DB": models.engine.url}