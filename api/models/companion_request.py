# CompanionRequest (Запрос на попутчика):
#     • • id (Primary Key) – уникальный идентификатор запроса.
# • user (ForeignKey на User, разместившего запрос).
# • start_location (начальная точка поездки).
# • end_location (конечная точка поездки).
# • date (дата и время поездки).
# • description (описание запроса, необязательное поле).
# • created_at (дата добавления запроса).

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column



from database import BaseModel



class CompanionRequest(BaseModel):
    __tablename__ = "companion_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped["User"] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="companion_requests")

    start_location: Mapped[str] = mapped_column(String(255), nullable=False)
    end_location: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime,  nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)