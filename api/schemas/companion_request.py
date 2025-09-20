from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
from typing import Optional
from datetime import datetime
from auth.schemas import UserSchema

class CompanionRequestCreateSchema(BaseModel):
    user_id: int
    start_location: str = Field(max_length=255)
    end_location: str = Field(max_length=255)
    date: datetime
    description: Optional[str] = Field(None, max_length=500)

    @field_validator('date')
    def validate_date(cls, value):
        
        current_time = datetime.now()  

        if value < current_time:
            raise ValueError("The trip date must be in the future.")
    
        return value

class CompanionRequestSchema(CompanionRequestCreateSchema):
    id: int
    user: UserSchema
    created_at: datetime

    class Config:
        orm_mode = True