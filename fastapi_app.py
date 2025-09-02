from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class LocationUpdate(BaseModel):
    bus_id: int
    latitude: float
    longitude: float

@app.post("/api/location/update")
async def update_location(location: LocationUpdate):
    # Here you would add logic to update the location in your database or cache
    # For testing, just return the received data
    return {"status": "success", "data": location.dict()}
