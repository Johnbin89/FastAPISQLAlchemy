from fastapi import APIRouter

router = APIRouter()


@router.get("/items/", tags=["users"])
async def read_items():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/items/{item_id}", tags=["users"])
async def read_item(item_id: str):
    return {"username": item_id}