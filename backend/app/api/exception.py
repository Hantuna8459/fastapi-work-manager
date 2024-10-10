from fastapi import HTTPException, status


InvalidUser = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Wrong username or password"
)

NotLogin = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not login"
)