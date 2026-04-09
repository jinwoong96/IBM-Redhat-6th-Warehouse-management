from fastapi import APIRouter, Depends, Response, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.db.scheme.users import UserRead, UserLogin, UserCreate, UserUpdate
from app.db.database import get_db
from app.services import UserService
from app.core.auth import set_auth_cookies, get_user_id



router = APIRouter(prefix="/users", tags=["User"])

# set_auth_cookies(response, access_token, refresh_token) : response객체에 쿠키로 토큰 저장
@router.post("/token")
async def login(user:UserLogin, response:Response, db:AsyncSession=Depends(get_db)):
    result = await UserService.login(db, user)
    db_user, access_token, refresh_token = result
    set_auth_cookies(response, access_token, refresh_token)
    return {"access_token":access_token}

@router.post("", response_model=UserRead)
async def signup(user:UserCreate, db:AsyncSession=Depends(get_db)):
    db_user = await UserService.signup(db, user)
    return db_user

@router.get("/me", response_model=UserRead)
async def get_me(user_id:int=Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    return await UserService.get_user(db, user_id)

@router.get("")
async def get_user_all(db:AsyncSession=Depends(get_db)):
    return await UserService.get_user_all(db)

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id:Annotated[int, Path(...)], db:AsyncSession=Depends(get_db)):
    return await UserService.get_user(db, user_id)

@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id:Annotated[int, Path(...)], user_data:UserUpdate, db:AsyncSession=Depends(get_db)):
    return await UserService.update_user(db, user_id, user_data)

@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(user_id:Annotated[int, Path(...)], db:AsyncSession=Depends(get_db)):
    return await UserService.delete_user(db, user_id)