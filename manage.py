import uvicorn

from fastapi import FastAPI

from database import BaseModel, engine

from auth.views import auth_router
from api.views.trip import trip_router
from api.views.companion_request import companion_router

app = FastAPI()

app.include_router(trip_router, prefix="/trips", tags=["Trips"])
app.include_router(companion_router, prefix="/companion_requests", tags=["Companion Requests"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=engine)
    uvicorn.run("manage:app", host="localhost", port=8000, reload= True)
