# Standard library
from datetime import datetime, timedelta

# libraries
from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

# Local app modules
from models.models import User
from schemas.schemas import (
    UserCreate, UserCreateResponse, UserLogin, Token, UserResponse,
    PasswordResetRequest, ResetPassword
)
from database.database import get_db, create_table
from auth.utils import hash_password, verify_password, generate_token, verify_token
from auth.jwt import create_access_token
from auth.oauth2 import get_current_active_user, RoleChecker
from services.mail import send_email

router = APIRouter(tags=['auth'])

@router.post('/register/', status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def register(request: UserCreate, db: Session = Depends(get_db)):
    # check if username or email already exists
    user = db.query(User).filter(
        (User.username == request.username) | (User.email == request.email)
    ).first()
    if user != None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already exists"
        )
    
    # hash password
    hashed_password = hash_password(request.password)

    # create user in db
    new_user = User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # email verification
    verification_token = generate_token(new_user.email)
    verification_link = f"http://127.0.0.1:8000/verify-email/?token={verification_token}"
    send_email(
        recipient=new_user.email,
        subject="Account Verification",
        body=f"Hi! Click this link to verify your email:\n\n{verification_link}"
    )

    return UserCreateResponse(
        message= "User account created successfully, verification email will be sent",
        data= new_user
    )

    ''' can also do
    return {
        "message": "User account created successfully, verification email will be sent",
        "data=": new_user
    }
    '''


@router.get('/verify-email/')
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):    # token is taken from the query parameter: /verify-email/?token=<the-token>
    token_data = verify_token(token=token, max_age=86400)
    email = token_data.get("email")

    if email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found to verify")
    
    if user.is_verified == True:
        return {"message": "user is already verified"}
    
    user.is_verified = True
    db.commit()
    db.refresh(user)

    return{
        "message":f"Email {user.email} sucessfully verified"
    }


@router.post('/login', response_model=Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavlid username or password")
    if user.is_verified != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not verified")
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # create access token
    access_token_expires = timedelta(minutes=30)
    # creating token using username
    access_token = create_access_token( 
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get('/protected')
def protected_route(current_user: User = Depends(get_current_active_user)):
    return {
        "message": "Access granted",
        "username": current_user.username
    }


@router.get('/all_users', response_model=list[UserResponse])
def get_all_users(_ = Depends(RoleChecker(allowed_roles=["admin", "user"])), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users



@router.put('/forget-password')
def forget_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    reset_token = generate_token(user.email)
    reset_link = f"http://127.0.0.1:8000/reset-password/?token={reset_token}"
    send_email(
        recipient=user.email,
        subject="Reset Password",
        body=f"Click this link to reset your password: \n\n {reset_link}"
    )

    return {
        "message": "Password Reset link has been sent"
    }

@router.post('/reset-password')
def reset_password(request: ResetPassword, reset_token: str = Query(...), db: Session = Depends(get_db)):
    token_data = verify_token(token=reset_token, max_age=900)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    email = token_data.get("email")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server err")

    new_password = request.new_password
    confirm_password = request.confirm_password

    if new_password != confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password Mismatch")

    hashed_password = hash_password(new_password)
    user.password = hashed_password

    db.commit()
    db.refresh(user)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Password Changed Successfully",
            "success": True,
            "status_code": status.HTTP_200_OK
        }
    )
    