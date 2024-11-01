from fastapi import FastAPI, HTTPException
from typing import List, Dict
from pydantic import BaseModel
import database
from datetime import datetime

app = FastAPI()

# Initiera databasen
database.initialize_database()

# Funktion för att validera datum
def validate_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'.")

# Definiera en modell för bokningsförfrågan
class BookingRequest(BaseModel):
    date: str
    time: str

# Klass för att hantera bokningssystemet
class BookingSystem:
    AVAILABLE_ROOMS = ['Room1', 'Room2', 'Room3', 'Room4', 'Room5']
    AVAILABLE_TIMES = [f"{hour}:00" for hour in range(10, 17)]  # Tider från 10:00 till 16:00 (boka till 17:00)

    def __init__(self):
        pass
    
    def book_room(self, room: str, date: str, time: str) -> bool:
        if room not in self.AVAILABLE_ROOMS:
            return False  # Rummet finns inte
        if time not in self.AVAILABLE_TIMES:
            return False  # Tiden är inte en av de tillgängliga tiderna
        
        # Kolla om rummet redan är bokat
        if database.book_room(room, date, time):
            return True
        return False

    def get_bookings(self) -> List[Dict]:
        return database.get_bookings()

# Instansiera bokningssystemet
booking_system = BookingSystem()

# API-rutter
@app.post("/book/{room}")
async def book_room_endpoint(room: str, booking_request: BookingRequest):
    # Validera datumet
    validate_date(booking_request.date)
    
    if booking_system.book_room(room, booking_request.date, booking_request.time):
        return {"message": f"{room} has been booked for {booking_request.date} at {booking_request.time}"}
    else:
        raise HTTPException(status_code=400, detail="Room could not be booked. It may already be booked or doesn't exist or the time is invalid.")

@app.get("/bookings")
async def get_all_bookings():
    return booking_system.get_bookings()
