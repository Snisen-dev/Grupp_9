from fastapi import FastAPI, HTTPException
from typing import List, Dict
import database  # Importera vår databasmodul

app = FastAPI()

# Initiera databasen
database.initialize_database()

# Klass för att hantera bokningssystemet
class BookingSystem:
    def book_room(self, room: str, date: str, time: str) -> bool:
        return database.book_room(room, date, time)

    def get_bookings(self) -> List[Dict]:
        return database.get_bookings()

# Instansiera bokningssystemet
booking_system = BookingSystem()

# API-rutter
@app.post("/book/{room}")
async def book_room_endpoint(room: str, date: str, time: str):
    if booking_system.book_room(room, date, time):
        return {"message": f"{room} has been booked for {date} at {time}"}
    else:
        raise HTTPException(status_code=400, detail="Room could not be booked. It may already be booked or doesn't exist.")

@app.get("/bookings")
async def get_all_bookings():
    return booking_system.get_bookings()
