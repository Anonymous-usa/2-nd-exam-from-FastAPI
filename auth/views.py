#      User (Пользователь):
#     • • Create: Регистрация нового пользователя.
# • Read: Просмотр информации о пользователе.
# • Update: Обновление информации о пользователе.
# • Delete: Удаление учетной записи.

from .models import User
from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserRegisterSchema, UserLoginSchema, UserSchema
from .handlers import token_response, generate_token, JWTBearer
from .utils import hash_password, verify_password, check_user
from database import get_db
from sqlalchemy.orm import Session

auth_router = APIRouter()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema, summary="Register a new user")
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

@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=UserSchema,  summary="Login a user")
async def login_user(user_data: UserLoginSchema, db: Session = Depends(get_db)):
    user = check_user(user_data)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return generate_token(user.id)

@auth_router.delete("/delete", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Delete a user")
async def delete_user(db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    user_id = token_response(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@auth_router.post("/logout", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())], summary="Logout a user")
async def logout_user():
    return {"message": "User logged out successfully"}

@auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserSchema, dependencies=[Depends(JWTBearer())])
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    user_id = token_response(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user






