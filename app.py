from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime, time
import sqlite3

app = FastAPI()

# Funktion för att ansluta till databasen
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Modell för bokningsförfrågan
class BookingRequest(BaseModel):
    room_id: int
    tid: str  # Tid i formatet "HH:MM"
    datum: str  # Datum i formatet "YYYY-MM-DD"

# Validera tidens format och om den är inom öppettider
def validate_time_format(tid: str) -> bool:
    try:
        tid_obj = datetime.strptime(tid, "%H:%M").time()
        return time(8, 0) <= tid_obj <= time(17, 0)
    except ValueError:
        return False

# GET-endpoint för att hämta alla lediga rum och tider för dagens datum
@app.get("/available-rooms", response_model=Dict[str, List[str]])
async def available_rooms():
    today = datetime.today().date()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT room, time FROM bookings WHERE date = ? AND available = 1", (today,))
    available_times = cursor.fetchall()
    conn.close()

    result = {}
    for row in available_times:
        room = row["room"]
        tid = row["time"]
        if room not in result:
            result[room] = []
        result[room].append(tid)

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Inga lediga rum finns för idag.")

# POST-endpoint för att boka ett rum
@app.post("/book-room")
async def book_room(data: BookingRequest):
    room_id = data.room_id
    tid = data.tid
    datum = data.datum

    # Validera tidens format och intervall
    if not validate_time_format(tid):
        raise HTTPException(status_code=422, detail="Ogiltigt tidsformat. Ange tiden i formatet HH:MM mellan 08:00 och 17:00.")

    # Förbered rums-ID
    room = f"Room {room_id}"

    # Anslut till databasen och kontrollera om tiden är ledig
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT available FROM bookings WHERE room = ? AND date = ? AND time = ?", (room, datum, tid))
    result = cursor.fetchone()

    # Om tiden är ledig, boka rummet
    if result and result["available"] == 1:
        cursor.execute("UPDATE bookings SET available = 0 WHERE room = ? AND date = ? AND time = ?", (room, datum, tid))
        conn.commit()
        conn.close()
        return {"message": f"Rummet {room} är nu bokat för {tid} den {datum}."}
    else:
        conn.close()
        raise HTTPException(status_code=409, detail=f"Rummet {room} är redan bokat för {tid} den {datum}. Välj en annan tid.")
