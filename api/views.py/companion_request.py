#      CompanionRequest (Запрос на попутчика):
#     • • Create: Добавление нового запроса.
# • Read: Просмотр списка запросов.
# • Update: Обновление информации о запросе.
# • Delete: Удаление запроса.

from auth.handlers import JWTBearer
from fastapi import APIRouter, Depends, status
from api.models.companion_request import CompanionRequest
from api.schemas.companion_request import CompanionRequestCreateSchema, CompanionRequestSchema
from database import get_db
from sqlalchemy.orm import Session

companion_router = APIRouter()

@companion_router.get("/", response_model=list[CompanionRequestSchema], dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, summary="Get all companion requests")
async def get_all_companion_requests(db: Session = Depends(get_db)):
    requests = db.query(CompanionRequest).all()
    return requests

@companion_router.get("/{request_id}", response_model=CompanionRequestSchema, dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, summary="Get a companion request by ID")
async def get_companion_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(CompanionRequest).filter(CompanionRequest.id == request_id).first()
    if not request:
        return {"error": "Companion request not found"}
    return request

@companion_router.post("/create", response_model=CompanionRequestSchema, dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED, summary="Create a new companion request")
async def create_companion_request(request_data: CompanionRequestCreateSchema, db: Session = Depends(get_db)):
    new_request = CompanionRequest(user_id=request_data.user_id, start_location=request_data.start_location,
                                    end_location=request_data.end_location, date=request_data.date,
                                     description=request_data.description)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@companion_router.delete("/{request_id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT, summary="Delete a companion request by ID")
async def delete_companion_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(CompanionRequest).filter(CompanionRequest.id == request_id).first()
    if not request:
        return {"error": "Companion request not found"}
    db.delete(request)
    db.commit()
    return {"message": "Companion request deleted successfully"}

@companion_router.put("/{request_id}", response_model=CompanionRequestSchema, dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, summary="Update a companion request by ID")
async def update_companion_request(request_id: int, request_data: CompanionRequestCreateSchema, db: Session = Depends(get_db)):
    request = db.query(CompanionRequest).filter(CompanionRequest.id == request_id).first()
    if not request:
        return {"error": "Companion request not found"}
    request.start_location = request_data.start_location
    request.end_location = request_data.end_location
    request.date = request_data.date
    request.description = request_data.description
    db.commit()
    db.refresh(request)
    return request
