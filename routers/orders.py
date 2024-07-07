from fastapi import APIRouter

router = APIRouter()


@router.get("/orders/", tags=["users"])
async def read_orders():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/orders/{order_id}", tags=["users"])
async def read_order(order_id: str):
    return {"username": order_id}