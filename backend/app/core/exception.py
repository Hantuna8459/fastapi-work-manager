from fastapi import HTTPException, status

EmailDuplicateException = HTTPException(
    status_code = status.HTTP_400_BAD_REQUEST,
    detail = "Email already registed"
)

UsernameDuplicateException = HTTPException(
    status_code = status.HTTP_400_BAD_REQUEST,
    detail = "Username already registed"
)

UnmatchedPasswordException = HTTPException(
    status_code = status.HTTP_400_BAD_REQUEST,
    detail = "Passwords do not match"
)

NoneDBException = HTTPException(
    status_code = status.HTTP_404_NOT_FOUND,
    detail = "Could not found"
)

CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)

InvalidUser = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Wrong username or password"
)

NotLogin = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not login"
)