# User (Пользователь):
#     • • id (Primary Key) – уникальный идентификатор пользователя.
# • username (никнейм пользователя).
# • email (электронная почта).
# • password (пароль).
# • created_at (дата регистрации).



from datetime import datetime
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column




from api.models.trip import Trip
from api.models.companion_request import CompanionRequest
from database import BaseModel



class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable= False)
    email: Mapped[str] = mapped_column(String(50),nullable=False )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    trips: Mapped[list["Trip"]] = relationship(back_populates="user")
    companion_requests: Mapped[list["CompanionRequest"]] = relationship(back_populates="user")
    