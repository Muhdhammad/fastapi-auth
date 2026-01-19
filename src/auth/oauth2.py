from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from auth.jwt import decode_token
from models.models import User
from schemas.schemas import TokenData
from database.database import get_db
from typing import Annotated, List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # paylaod is data of the token
        payload = decode_token(token=token)
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data
    
    except jwt.PyJWTError:
        raise credentials_exception

# So this is a dependency on the above function
def get_current_active_user(current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    if user.is_verified != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not verified")
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[User, Depends(get_current_active_user)]):
        if user.role in self.allowed_roles:
            return user
        else: 
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have enough permissions")
        