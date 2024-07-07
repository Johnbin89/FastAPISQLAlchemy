from fastapi import Depends, FastAPI
from .models import models as models
from .routers import items, customers, orders


models.Base.metadata.create_all(bind=models.engine)
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
    return {"message": "Hello Bigger Applications!"}