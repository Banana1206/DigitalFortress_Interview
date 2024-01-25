from fastapi import APIRouter, HTTPException
from schemas import User, CurrentPosition
from services import get_all_user, get_all_island, compute_distance, add_user, get_user
import pandas as pd
from schemas import Register, Token

router = APIRouter()


@router.post("/register", response_model=User)
def register(user: Register):
    return add_user(user)

@router.post("/login", response_model=User)
def login(username: Token):
    try: 
        user = get_user(username.username)
        if username.username != user.username:
            raise HTTPException(status_code=401, detail="Invalid password")
        return user
    except:
        raise HTTPException(status_code=404, detail="User not found") 
    
@router.get("/users")
def get_all_of_user():
    return get_all_user()   


@router.post("/islands")
def get_islands(current_pos: CurrentPosition):
    # print(current_pos.latitude)
    # print(type(current_pos))
    data =get_all_island()
    # Convert the result to a DataFrame
    df = pd.DataFrame([
        {"island_id": island.island_id, "name": island.name, "longitude": island.longitude, 
         "latitude": island.latitude, "area": island.area, "description": island.description}
        for island in data
    ])
    
    df['distance_km'] = df.apply(lambda row: compute_distance(
        current_pos.latitude, current_pos.longitude, row['latitude'], row['longitude']), axis=1)
    
    # Sort the DataFrame by distance
    df = df.sort_values(by='distance_km')
    
    # Drop the distance column if you don't want to include it in the response
    df = df.drop(columns=['distance_km'])

    return df.to_dict(orient='records')

