from fastapi import HTTPException, status

CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

InvalidUser = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Wrong username or password"
)

NotLogin = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not login"
)