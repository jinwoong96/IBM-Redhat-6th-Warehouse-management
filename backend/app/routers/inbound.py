from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.core.auth import set_auth_cookies, get_user_id


router = APIRouter(prefix="/inbounds", tags=["Inbound"])