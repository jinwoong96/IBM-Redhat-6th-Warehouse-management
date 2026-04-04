from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated


class OutboundBase(BaseModel):
    order_id:int
    product_id:int
    location:int
    outbound_qty:int
    outbound_date:datetime

class OutboundCreate(BaseModel):
    order_id:int
    product_id:int
    location:int
    outbound_qty:int=Field(ge=1)
    outbound_date:datetime

class OutboundUpdate(BaseModel):
    outbound_qty:int | None=None
    outbound_date:datetime | None=None

class OutboundInDB(OutboundBase):
    outbound_id: int

    class Config:
        from_attributes = True

class OutboundRead(OutboundInDB):
    pass