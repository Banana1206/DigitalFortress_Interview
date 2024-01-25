from fastapi import FastAPI, Request
from database import engine
from models import Base
from views import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)