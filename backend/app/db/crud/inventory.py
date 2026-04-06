from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Inventory


class InventoryCrud:

    @staticmethod
    async def get_by_id(db:AsyncSession, product_id:int | None = None,
                                         location_id:int | None = None) -> list[Inventory]:
        
        semiresult = select(Inventory)

        if product_id:
            semiresult = semiresult.filter(Inventory.product_id == product_id)
        if location_id:
            semiresult = semiresult.filter(Inventory.location_id == location_id)

        result = await db.execute(semiresult)

        return result.scalars.all()