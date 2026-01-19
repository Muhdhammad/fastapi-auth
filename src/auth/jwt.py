from fastapi import HTTPException, status
from datetime import datetime, timezone, timedelta
from config import Config
import jwt
import uuid

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    jti = str(uuid.uuid4()) # unique identifier
    to_encode.update({"jti": jti})

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    token = jwt.encode(payload=to_encode, key=Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGO)

    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            token,
            Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGO]
        )
        return token_data
    
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )