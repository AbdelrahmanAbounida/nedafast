from typing import Optional
from pydantic import BaseModel, Field
from typing import Annotated
from beanie import Document, Indexed, init_beanie


class Category(BaseModel):
    name: str
    description: str

class Item(Document):
    name: str                         
    description: Optional[str] = None
    price: Annotated[float,Indexed(float)]      
    category: Category                 




# CRUD Schemas 
class CreateItemSchema(BaseModel):
    name: str
    description: Optional[str] = Field(default=None, description="Optional description of the item")
    price: float
    category: Category