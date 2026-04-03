from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User
from app.db.scheme.users import UserCreate, UserUpdate


# User 테이블과 관련된 CRUD작업을 모아둔 클래스
# scalar_one_or_none : 결과 1개면 객체반환, 없으면 none반환
class UserCrud:
    @staticmethod
    async def get_by_id(db:AsyncSession, user_id:int) -> User|None:
        result = await db.execute(select(User).filter(User.user_id==user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db:AsyncSession, user:UserCreate) -> User:
        db_user=User(**user.model_dump())
        db.add(db_user)
        await db.flush()
        return db_user
    
    # model_dump(exclude_unset=True) : pydantic에서 명시적으로 설정된 필드만 추출(딕셔너리)
    @staticmethod
    async def update_by_id(db:AsyncSession, user_id:int, user:UserUpdate) -> User|None:
        db_user = await db.get(User, user_id)
        if db_user:
            update_data = user.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_user, key, value)  # db_user.key=value
            await db.flush()
            return db_user
        return None
    
    @staticmethod
    async def delete_by_id(db: AsyncSession, user_id: int) -> User | None:
        db_user = await db.get(User, user_id)
        if db_user:
            await db.delete(db_user)
            await db.flush()
            return db_user
        return None

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()
    
    # 리프레시 토큰 왜 DB에 저장? 재사용방지
    # 오래 살아있기 때문에 윺출되면 내가 아닌 제 3자가 계속 새 액세스 토큰 발급받을 수 있다.
    # 보안강화 -> 서버에서 검증하려고(db와 비교해서)

    # 사용자 로그인 -> 새 리프레시토큰 발급 -> db에 저장
    # 액세스토큰이 만료되면 사용자가 리프레시토큰 전송
    # 서버에서 db 확인. 토큰 일치 -> 새 액세스 토큰 발급 / 일치안함 -> 거부
    @staticmethod
    async def update_refresh_token_by_id(
        db:AsyncSession, user_id:int, refresh_token:str):

        db_user = await db.get(User, user_id)
        if db_user:
            db_user.refresh_token = refresh_token
            await db.flush()
        return db_user