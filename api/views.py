from fastapi import APIRouter, HTTPException
from schemas import User, CurrentPosition
from services import get_all_user, get_all_island, compute_distance, add_user, get_user
import pandas as pd
from schemas import Register, Token

router = APIRouter()

# ================================================================
# Phase 1

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


# ================================================================
# Phase 2

@router.post("/islands")
def get_distances(current_pos: CurrentPosition):
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

# ================================================================
# Phase 3
from collections import deque

# image = [
#   ["1","1","1","1","0"],
#   ["1","1","0","1","0"],
#   ["1","1","0","0","0"],
#   ["0","0","0","0","0"]
# ]

image = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]

@router.get("/islands_from_image")
def get_islands_from_image():
    m, n = len(image), len(image[0])
    island_count = 0
    visited = [[False] * n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            if image[i][j] == "1" and not visited[i][j]:
                island_count += 1
                visited[i][j] = True
                island_id = island_count  # Use this to create island record in database
                queue = deque([(i, j)])

                while queue:
                    current_i, current_j = queue.popleft()
                    # Explore all four directions within image boundaries
                    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        new_i, new_j = current_i + di, current_j + dj
                        if 0 <= new_i < m and 0 <= new_j < n and image[new_i][new_j] == "1" and not visited[new_i][new_j]:
                            queue.append((new_i, new_j))
                            visited[new_i][new_j] = True
                            # For each visited land cell, create an island record in the database:
                            # create_island_record(island_id, new_i, new_j)  # Adapt this line to your database logic

    return {"number of island(s)":island_count}
        



