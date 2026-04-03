from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated


class ProductBase(BaseModel):
    product_name:str
    category:str
    price:int

class ProductCreate(BaseModel):
    product_name:str=Field(le=50)
    category:str=Field(le=40)
    price:int=Field(ge=0)

class ProductUpdate(BaseModel):
    product_name:str | None=None
    category:str | None=None
    price:int | None=None

class ProductInDB(ProductBase):
    product_id: int

    class Config:
        from_attributes = True

class ProductRead(ProductInDB):
    pass