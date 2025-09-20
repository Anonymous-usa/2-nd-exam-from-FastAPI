from .models import User
from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserRegisterSchema, UserLoginSchema, UserSchema
from .handlers import token_response, generate_token, JWTBearer
from .utils import hash_password, verify_password, check_user
from database import get_db
from sqlalchemy.orm import Session

auth_router = APIRouter()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def register_user(user_data: UserRegisterSchema, db: Session = Depends(get_db)):
    existing_user = check_user(user_data)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    password_hashed = hash_password(user_data.password)
    user = User(username=user_data.username, email=user_data.email, hashed_password=password_hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully", "user": user}

@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def login_user(user_data: UserLoginSchema, db: Session = Depends(get_db)):
    user = check_user(user_data)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return generate_token(user.id)


@auth_router.post("/logout", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def logout_user():

    return {"message": "User logged out successfully"}




