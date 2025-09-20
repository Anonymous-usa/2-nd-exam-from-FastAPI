from passlib.hash import bcrypt
from .schemas import UserRegisterSchema
from database import LocalSession
from .models import User


def hash_password(password: str):
    return bcrypt.hash(password)

def verify_password(password: str, hashed_password: str):
    return bcrypt.verify(password, hashed_password)

def check_user(user:UserRegisterSchema):
    db = LocalSession()
    user = db.query(User).filter(User.username == user.username).first()
    db.close()
    if user:
        return user
    return None