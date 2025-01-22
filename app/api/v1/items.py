from fastapi.routing import APIRouter
from app.database.cruds import create_item, get_items
from app.database.models.items import CreateItemSchema



router = APIRouter(tags=["ITems Router"],prefix="/item")


@router.get("/")
async def get_items_route():
    items = await get_items() 
    print(1/0)
    return items 
 

@router.post("/")
async def create_item_route(body:CreateItemSchema):
    item = await create_item(body)
    return item  