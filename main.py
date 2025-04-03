from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Store vehicle location
vehicle_location = {"latitude": 28.7041, "longitude": 77.1025}

class LocationUpdate(BaseModel):
    latitude: float
    longitude: float

@app.post("/api/update-location")
def update_location(data: LocationUpdate):
    """Update vehicle's location (Simulated GPS)"""
    global vehicle_location
    vehicle_location = data.dict()
    return {"message": "Location updated"}

@app.get("/api/get-location")
def get_location():
    """Get latest vehicle location"""
    return vehicle_location
