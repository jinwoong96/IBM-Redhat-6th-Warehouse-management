from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated


class LocationBase(BaseModel):
    location_name:str
    zone:str

class LocationCreate(BaseModel):
    location_name:str=Field(le=50)
    zone:str=Field(le=50)

class InventoryUpdate(BaseModel):
    location_name:str | None=Field(le=50)
    zone:str | None=Field(le=50)

class LocationInDB(LocationBase):
    location_id:int
    
    class Config:
        from_attributes = True

class InventoryRead(LocationInDB):
    pass