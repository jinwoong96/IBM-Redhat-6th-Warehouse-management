from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.db.models import Inbound
from app.db.scheme.inbounds import InboundCreate, InboundRead
from app.db.crud import InboundCrud


class InboundService:
    @staticmethod
    async def get_inbounds(db:AsyncSession, product_id, location_id):
        query = select(Inbound)
        if product_id:
            query = query.filter(Inbound.product_id==product_id)
        if location_id:
            query = query.filter(Inbound.location_id==location_id)
        query = query.order_by(Inbound.inbound_id.desc())
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create(db:AsyncSession, inbound_create:InboundCreate) -> InboundRead:
        try:
            db_inbound = await InboundCrud.create(db, inbound_create)
            await db.commit()
            await db.refresh(db_inbound)
            return db_inbound
        except:
            await db.rollback()
            raise
            
