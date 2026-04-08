from fastapi import Request, HTTPException
from app.core.jwt_handle import verify_token
from jwt import ExpiredSignatureError, InvalidTokenError

async def check_login(request:Request):

    # 쿠키에서 access 토큰 가져옴
    access_token = request.cookies.get("access_token")

    # 액세스토큰 존재하면, 유효성 검증 => 만료/잘못된 토큰이면 pass -> 리프레시로 이동
    try:
        if not access_token:
            raise HTTPException(status_code=401, detail="로그인 해야 사용가능")
        verify_token(access_token)            
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰 만료됨")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰")