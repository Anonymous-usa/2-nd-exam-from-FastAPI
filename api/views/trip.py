#      . Trip (Поездка):
#     • • Create: Добавление новой поездки.
# • Read: Просмотр доступных поездок.
# • Update: Обновление информации о поездке.
# • Delete: Удаление поездки.


from auth.handlers import JWTBearer
from fastapi import APIRouter, Depends, status
from api.models.trip import Trip
from api.schemas.trip import TripCreateSchema, TripSchema
from database import get_db
from sqlalchemy.orm import Session

trip_router = APIRouter()

@trip_router.get("/", response_model=list[TripSchema], dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, summary="Get all trips")
async def get_all_trips(db: Session = Depends(get_db)):
    trips = db.query(Trip).all()
    return trips

@trip_router.get("/{trip_id}", response_model=TripSchema, dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, summary="Get a trip by ID" )
async def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        return {"error": "Trip not found"}
    return trip

@trip_router.post("/create", response_model=TripSchema, dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED, summary="Create a new trip")
async def create_trip(trip_data: TripCreateSchema, db: Session = Depends(get_db)):
    new_trip = Trip(user_id=trip_data.user_id,  start_location=trip_data.start_location,
                    end_location=trip_data.end_location, date=trip_data.date,
                    seats_available=trip_data.seats_available, description=trip_data.description)
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip

@trip_router.delete("/{trip_id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT, summary="Delete a trip by ID")
async def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        return {"error": "Trip not found"}
    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted successfully"}

@trip_router.put("/{trip_id}", response_model=TripSchema, dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, summary="Update a trip by ID")
async def update_trip(trip_id: int, trip_data: TripCreateSchema, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        return {"error": "Trip not found"}
    trip.start_location = trip_data.start_location
    trip.end_location = trip_data.end_location
    trip.date = trip_data.date
    trip.seats_available = trip_data.seats_available
    trip.description = trip_data.description
    db.commit()
    db.refresh(trip)
    return trip

