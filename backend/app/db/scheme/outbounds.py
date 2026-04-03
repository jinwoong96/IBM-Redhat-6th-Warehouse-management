from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated


class OutboundBase(BaseModel):
    pass