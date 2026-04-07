from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud import LocationCrud
from app.db.scheme.locations import LocationCreate, LocationUpdate

class LocationService:
    async def create_location_service(db: AsyncSession, location_data: LocationCreate):
        return await LocationCrud.create_location(db, location_data)

    async def get_location_by_id_service(db: AsyncSession, location_id: int):
        db_location = LocationCrud.get_location_by_id(db, location_id)
        if not db_location:
            raise HTTPException(status_code=404, detail="Location not found")
        return await db_location


    async def update_location_service(db: AsyncSession, location_id: int, location_data: LocationUpdate):
        db_location = await LocationCrud.get_location_by_id(db, location_id)
        if not db_location:
            raise HTTPException(status_code=404, detail="Location not found")
        return await LocationCrud.update_location(db, db_location, location_data)


    async def delete_location_service(db: AsyncSession, location_id: int):
        db_location = await LocationCrud.get_location_by_id(db, location_id)
        if not db_location:
            raise HTTPException(status_code=404, detail="Location not found")
        LocationCrud.delete_location(db, db_location)
        return {"msg": "삭제 성공"}