from datetime import datetime, timedelta

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    email: str
    
class Token(BaseModel):
    username: str
    password: str

class Register(BaseModel):
    username: str
    password: str
    email: str
    
class CurrentPosition(BaseModel):
    longitude: float
    latitude: float
    