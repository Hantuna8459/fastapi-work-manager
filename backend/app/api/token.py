from datetime import timedelta

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from backend.app.core.exception import CredentialsException
from backend.app.core.auth import SECRET_KEY, ALGORITHM, get_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from backend.app.core.database import get_db

def get_old_refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    else:
        return refresh_token

def make_new_access_token(request: Request, db = Depends(get_db)):
    # Lấy refresh token từ cookies
    refresh_token = get_old_refresh_token(request)

    try:
        # Giải mã refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException
    except JWTError:
        raise CredentialsException

    # Kiểm tra xem người dùng có tồn tại không
    user = get_user(db, username=username)
    if user is None:
        raise CredentialsException

    # Tạo access token mới
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
