from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.core.auth import set_auth_cookies, get_user_id
from app.services import InventoryService


router = APIRouter(prefix="/inventorys", tags=["Inventory"])

@router.get("")
async def get_inventorys(product_id:int=Query(None), location_id:int=Query(None), db:AsyncSession=Depends(get_db)):
    return await InventoryService.get_inventorys(db, product_id, location_id)