from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from app.core.settings import settings
import uuid


# 해싱방식과 정책관리 (bcrypt 알고리즘 사용)
pwd_crypt = CryptContext(schemes=["bcrypt"])

def get_password_hash(password:str):
    trunc_password = password.encode('utf-8')[:72]
    return pwd_crypt.hash(trunc_password)

# 평문 비번과 해시값 비교해서 같으면 true
def verify_password(plain_pw:str, hashed_pw:str) -> bool:
    trunc_password = plain_pw.encode('utf-8')[:72]
    return pwd_crypt.verify(trunc_password, hashed_pw)

def create_token(uid:int, expires_delta:timedelta, **kwargs) -> str:
    to_encode=kwargs.copy() #추가정보를 페이로드에 넣고 싶을 때 
    expire=datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp":expire, "uid":uid})
    encoded_jwt=jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

# create_token함수 호출해서 jwt 생성 -> uid, exp 포함 -> kwargs없으면 payload는 uid, exp만 있음
def create_access_token(uid:int)->str:
    return create_token(uid=uid, expires_delta=settings.access_token_expire)

#리프레시 토큰 관리(재발급/ 로그아웃 시 무효화)
# jti (jwt_id): 서버에서 토큰 재사용 방지 관리 기능
# uuid : 전세계에서 유일하게 식별할 수 있는 128비트 값 생성
def create_refresh_token(uid:int):
    return create_token(uid=uid, jti=str(uuid.uuid4()), expires_delta=settings.refresh_token_expire)

# 토큰을 디코딩해서 payload를 딕셔너리로 반환
# 서명을 검증해서 토큰의 변조 여부를 확인
def decode_token(token:str) -> dict:
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.jwt_algorithm]
    )

# 토큰을 디코딩한 후 uid값을 꺼낸다 -> 사용자 id
def verify_token(token:str)->int:
    payload = decode_token(token)
    return payload.get("uid")