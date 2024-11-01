# Import necessary modules
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime, timedelta
from development import get_db_connection  # Importera korrekt funktion för databasanslutning

app = FastAPI()

# Modell för bokningsförfrågan
class BookingRequest(BaseModel):
    room_id: int
    tid: str
    datum: str  # Datum som användaren skickar in i formatet "YYYY-MM-DD"

# Funktion för att validera tidens format och intervall
def validate_time_format(tid: str) -> bool:
    try:
        tid_obj = datetime.strptime(tid, "%H:%M").time()
        return timedelta(hours=8) <= timedelta(hours=tid_obj.hour) <= timedelta(hours=17)
    except ValueError:
        return False

# Funktion för att ansluta till databasen
def connect_to_db():
    try: 
        connection = get_db_connection()
        return connection
    except Exception as e:
        print(f'Error connecting to database: {e}')
        return None

# Klass för att representera ett rum
class Room:
    def __init__(self, id: int, booked: bool = False) -> None:
        self.id = id
        self.booked = booked
    
    def to_dict(self) -> Dict:
        return {"id": self.id, "booked": self.booked}

# Klass för att hantera alla rum
class AllRooms:
    def __init__(self) -> None:
        self.rooms: List[Room] = []

