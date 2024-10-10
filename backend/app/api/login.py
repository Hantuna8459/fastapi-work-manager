from backend.app.api.util import verify_password
from backend.app.api.exception import InvalidUser
from backend.app.core import auth
from backend.app.api.schema import UserLogin


def login(db, user: UserLogin)
    
    db_user = auth.get_user(db, user.username)
    if (not db_user) or (not verify_password(user.password, db_user.password)):
        raise InvalidUser
    
    token = auth.create_access_token({"id": user.id})
    refresh_token = auth.create_refresh_token({"id": user.id})
                       
    return {"access_token": token, "refresh_token": refresh_token}
