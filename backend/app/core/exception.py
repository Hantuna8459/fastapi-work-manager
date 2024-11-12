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

UserNotActiveException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User does not active"
)

CategoryNameAlreadyUsed = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="category name is already used",
)

NotCreatorOfCategory = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You are not creator of this category",
)

CantAccessCategory = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You don't have permission to access this category",
)

CategoryNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="category not found",
)

TodoItemNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Todo item not found.",
)

CantAccessTodoItem = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You don't have permission to access this todo item."
)

NotCreatorOfTodoItem = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You are not creator of this todo item."
)

UserJoinedCategory = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User is already joined this category."
)

UserNotJoinedCategory = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User is not joined this category."
)

SomeThingWentWrong = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Some thing went wrong, please try again later."
)

class TodoItemStatusDoneException(Exception):
    def __init__(self):
        self.message = "Todo Item is Done!"
        super().__init__(self.message)