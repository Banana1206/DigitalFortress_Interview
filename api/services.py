from typing import Optional
from database import session
from models import User, Island
from schemas import Register
from math import radians, sin, cos, sqrt, atan2


def get_user(username: str) -> Optional[User]:
    with session() as db:
        return db.query(User).filter(User.username == username).one_or_none()

def add_user(user: Register) -> Optional[User]:
    db_user = User(**user.dict())
    with session() as db:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def get_all_user():
    with session() as db:
        return db.query(User).all()
    
def get_all_island():
    with session() as db:
        return db.query(Island).all()
    
def compute_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = R * c

    return distance
