from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, async_engine
from fastapi.concurrency import asynccontextmanager
from dotenv import load_dotenv
from app.middleware.token_refresh import RefreshTokenMiddleware
from app.routers import user

load_dotenv(dotenv_path=".env")

# 애플리케이션의 시작과 종료 시 실행될 작업을 정의함
# 시작/끝을 비동기적으로 처리
@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(RefreshTokenMiddleware)

# CORSMiddleware : 다른도메인, 포트에서 오는 요청을 허용하도록 하는 미들웨어
# allow_origins : 요청을 허용할 출처 리스트
# allow_credentials : 로그인/jwt 기반 인증 필요한 경우(쿠키, 세션정보 등 요청 허용)
# allow_methods : HTTP 모든 메소드 다 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 라우터 만든거 추가해주기
app.include_router(user.router)
