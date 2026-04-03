from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.scheme.users import UserRead, UserLogin, UserCreate
from app.db.database import get_db
from app.services import UserService
from app.core.auth import set_auth_cookies, get_user_id



router = APIRouter(prefix="/users", tags=["User"])

@router.get("/me", response_model=UserRead)
async def get_user(user_id:int=Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    return await UserService.get_user(db, user_id)

@router.post("/signup", response_model=UserRead)
async def signup(user:UserCreate, db:AsyncSession=Depends(get_db)):
    db_user = await UserService.signup(db, user)
    return db_user

# set_auth_cookies(response, access_token, refresh_token) : response객체에 쿠키로 토큰 저장
@router.post("/login", response_model=UserRead)
async def login(user:UserLogin, response:Response, db:AsyncSession=Depends(get_db)):
    result = await UserService.login(db, user)
    db_user, access_token, refresh_token = result
    set_auth_cookies(response, access_token, refresh_token)
    return db_user

# 로그아웃 시 액세스/리프레시 토큰 쿠키 삭제
@router.post("/logout", response_model=bool)
async def logout(response:Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return True