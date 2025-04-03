from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from geopy.distance import geodesic
import asyncio

app = FastAPI()

# Simulated bus location (initial location: Example - New York)
bus_location = {"latitude": 40.7128, "longitude": -74.0060, "speed_kmph": 40}  # Speed in km/h

# Define some bus stops (latitude, longitude)
bus_stops = {
    "Stop 1": (40.7306, -73.9352),  # Example: Manhattan
    "Stop 2": (40.7498, -73.9876),  # Example: Times Square
    "Stop 3": (40.7580, -73.9855),  # Example: Central Park
}

# WebSocket clients for real-time updates
clients = []


class LocationUpdate(BaseModel):
    latitude: float
    longitude: float
    speed_kmph: float  # Speed of the bus


@app.post("/api/update-location")
async def update_location(data: LocationUpdate):
    """Update the real-time location of the bus"""
    global bus_location
    bus_location.update(data.dict())

    # Send update to all WebSocket clients
    for client in clients:
        await client.send_json({"latitude": data.latitude, "longitude": data.longitude})
    
    return {"message": "Bus location updated successfully"}


@app.get("/api/get-location")
def get_location():
    """Get the latest bus location"""
    return bus_location


@app.get("/api/get-eta")
def get_eta():
    """Estimate the time of arrival at each bus stop"""
    eta_data = {}

    for stop, coordinates in bus_stops.items():
        distance_km = geodesic((bus_location["latitude"], bus_location["longitude"]), coordinates).km
        eta_minutes = (distance_km / bus_location["speed_kmph"]) * 60  # Convert hours to minutes
        eta_data[stop] = round(eta_minutes, 2)  # Round to 2 decimal places

    return eta_data


@app.websocket("/ws/location")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time bus location updates"""
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            await asyncio.sleep(2)  # Send update every 2 seconds
            await websocket.send_json(bus_location)
    except Exception as e:
        clients.remove(websocket)


@app.get("/")
def home():
    return {"message": "Real-Time Bus Tracking API is Running!"}
