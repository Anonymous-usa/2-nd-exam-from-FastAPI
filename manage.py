import uvicorn

from fastapi import FastAPI

from database import BaseModel, engine

app = FastAPI()


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=engine)
    uvicorn.run("manage:app", host="localhost", port=8000, reload= True)
