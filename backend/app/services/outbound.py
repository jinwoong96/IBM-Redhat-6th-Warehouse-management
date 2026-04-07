from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.db.models import Outbound
from app.db.scheme.outbounds import OutboundCreate, OutboundRead
from app.db.crud import OutboundCrud

class OutboundService:
    @staticmethod
    async def get_outbounds(db:AsyncSession, product_id, location_id):
        query = select(Outbound)
        if product_id:
            query = query.filter(Outbound.product_id==product_id)
        if location_id:
            query = query.filter(Outbound.location_id==location_id)
        query = query.order_by(Outbound.outbound_id.desc())
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create(db:AsyncSession, outbound_create:OutboundCreate) -> OutboundRead:
        try:
            db_outbound = await OutboundCrud.create(db, outbound_create)
            await db.commit()
            await db.refresh(db_outbound)
            return db_outbound
        except:
            await db.rollback()
            raise