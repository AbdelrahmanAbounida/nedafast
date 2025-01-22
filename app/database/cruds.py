from app.database.models.items import  CreateItemSchema, Item


async def create_item(body:CreateItemSchema):
    item  = Item(**body.model_dump())
    await item.insert()
    return item 


async def get_items():
    items =   await Item.find_all().to_list()
    return items 