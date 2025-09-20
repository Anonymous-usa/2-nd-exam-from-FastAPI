from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
from typing import Optional
from datetime import datetime

class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    @field_validator("*", mode="before")
    def check_all(value):
        if value is None:
            raise ValueError("All fields  are required")
        return value

    @model_validator("confirm_password", mode="before")
    def check_passwords(self):
        if self["password"] != self["confirm_password"]:
            raise ValueError("Passwords do not match")
        return self
    
class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class UserLoginSchema(BaseModel):
    username: str
    password: str

    @field_validator("*", mode="before")
    def check_all(value):
        if value is None:
            raise ValueError("All fields  are required")
        return value
    
