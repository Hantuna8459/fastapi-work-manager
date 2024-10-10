# api end point here

auth_router = APIRouter(prefix="auth")

@auth_router.post("/refresh-token")
def refresh_token(response: Response, db: Session = Depends(get_db), refresh_token: Optional[str] = None):
    # Lấy refresh token từ cookies
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        # Giải mã refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Kiểm tra xem người dùng có tồn tại không
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception

    # Tạo access token mới
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    # Xóa cookie bằng cách đặt thời gian hết hạn
    response.delete_cookie(key="refresh_token")
    return {"msg": "Logged out"}
