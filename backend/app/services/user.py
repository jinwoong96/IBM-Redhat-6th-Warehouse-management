# MVC
# Model(DB, ORM) - scheme(pydantic - DTO) - service(비즈니스 로직)
# View
# Controller(Router)


# 1. 클라이언트가 http 요청
# 2. router가 요청 url과 매핑 @app.post("/aa")
# 3. pydantic으로 요청데이터 검증
# 4. service 호출 (db와 상호작용 model) -> 결과반환
# 5. Json응답으로 클라이언트에게 전송

# 1. 클라이언트 -> router -> scheme로 데이터 검증 -> router -> service 호출
# -> model/db crud 수행 -> 결과반환 -> response 반환

# Router -> Service -> Model -> DB -> Service -> Router -> Response

# scheme(user.py) / crud -> serivce -> router(contoller) -> front
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.db.scheme.users import UserCreate, UserUpdate, UserLogin
from sqlalchemy.future import select
from app.db.crud import UserCrud
from fastapi import HTTPException
from app.core.jwt_handle import (
    create_access_token,
    create_refresh_token,
    get_password_hash, 
    verify_password
)

# crud는 UserCrud에서 처리하고, 비즈니스 규칙(유효성검사, 비밀번호해시, 예외처리 등)을 추가
class UserService:

    @staticmethod
    async def get_user(db:AsyncSession, user_id:int) -> User:
        db_user = await UserCrud.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="사용자 찾을 수 없다")
        return db_user

    @staticmethod
    async def signup(db:AsyncSession, user:UserCreate):
        #중복 username확인
        if await UserCrud.get_by_username(db, user.username):
            raise HTTPException(status_code=400,  detail="이미 사용중인 이름이다")
        
        #username없으면 -> username, password, email을 디비에 저장해야함
        hash_pw=get_password_hash(user.password) #비번 암호화해서 들어감
        user_create=UserCreate(username=user.username, password=hash_pw, email=user.email)

        try:
            db_user=await UserCrud.create(db,user_create)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        
        except Exception:
            raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비번이다")

    @staticmethod
    async def login(db:AsyncSession, user:UserLogin):
        # get_email함수호출
        db_user=await UserCrud.get_by_email(db, user.email)

        #디비에 들어잇는 암호화된 비번과 내가 입력한 비번 확인
        if not db_user or not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비번이다")
        
        refresh_token=create_refresh_token(db_user.user_id)
        access_token=create_access_token(db_user.user_id)

        updated_user = await UserCrud.update_refresh_token_by_id(db, db_user.user_id, refresh_token)
        await db.commit()
        await db.refresh(updated_user)
        
        return updated_user, access_token, refresh_token
    
    #1. 이메일+비번 -> 인증
    #2. jwt 액세스/리프레시 토큰 발급
    #3. 리프레시토큰 db저장
    #4. db커밋 후 사용자 객체 최신화
    #5. 사용자 정보 + jwt 액세스/리프레시 토큰 반환