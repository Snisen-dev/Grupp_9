<<<<<<< Updated upstream:app.py
# Import nessecairy modules
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from development import get_db_connection as con_db

app = FastAPI()

# Functionn for connecting to the database
def connect_to_db():
    try: 
        connection = con_db()
        return connection
    except Exception as e:
        print(f'Error connecting to database: {e}')
        return None

# Initiate a class Room, giving it an id and a boolean
class Room:
    def __init__(self, id: int, booked: bool = False) -> None:
        self.id = id
        self.booked = booked
    
    # Function for returning the "room", to a dict format, compatible with JSON
    def to_dict(self) -> Dict:
        return {"id": self.id, "booked": self.booked}

class AllRooms:
    def __init__(self) -> None:
        self.rooms: List[Room] = []
        self.db_connection = connect_to_db()

    # 
    def new_room(self, room_id: int):
        self.rooms.append(Room(id=room_id))

    # Function for booking a room, if the room is not booked
    def book_room(self, room_id: int) -> bool:
        for room in self.rooms:
            if room.id == room_id and not room.booked:
                room.booked = True
                return True
        return False

    def get_all_rooms(self) -> List[Dict]:
        return [room.to_dict() for room in self.rooms]
=======
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime, time, timedelta
from development import get_db_connection  

app = FastAPI()

# Modell för bokningsförfrågan
class BookingRequest(BaseModel):
    room_id: int
    tid: str
    datum: str  # Datum som användaren skickar in

# Funktion för att validera tidens format och intervall
def validate_time_format(tid: str) -> bool:
    try:
        tid_obj = datetime.strptime(tid, "%H:%M").time()
        return time(8, 0) <= tid_obj <= time(17, 0)
    except ValueError:
        return False

@app.get("/available-rooms-week", response_model=Dict[str, Dict[str, List[str]]])
async def available_rooms_week():
    today = datetime.today().date()
>>>>>>> Stashed changes:app_dev.py

    # Hämta alla dagar från måndag till fredag för denna vecka
    weekdays = [today + timedelta(days=i) for i in range(7) if (today + timedelta(days=i)).weekday() < 5]

<<<<<<< Updated upstream:app.py
    def get_unbooked_rooms(self) -> List[Dict]:
        return [room.to_dict() for room in self.rooms if not room.booked]

booking_system = AllRooms()

# Add some rooms for testing
for i in range(1, 6):
    booking_system.new_room(i)

@app.get("/")
async def root():
    return {'Message': 'Välkommen till Grupp 9:s bokningssystem'}

@app.get("/rooms")
async def check_bookings():
    return booking_system.get_all_rooms()

@app.get("/rooms/booked")
async def booked_rooms():
    return booking_system.get_booked_rooms()

@app.get("/rooms/unbooked")
async def unbooked_rooms():
    return booking_system.get_unbooked_rooms()

@app.post("/book/{room_id}")
async def new_booking(room_id: int):
    if booking_system.book_room(room_id):
        return {"message": f"Room {room_id} has been booked"}
=======
    conn = get_db_connection()
    cursor = conn.cursor()

    # Samla lediga tider för varje veckodag och rum
    week_availability = {}
    for day in weekdays:
        date_str = day.isoformat()
        cursor.execute("SELECT rum_id, tid FROM bookings WHERE datum = ? AND available = 1", (date_str,))
        available_times = cursor.fetchall()
        
        day_availability = {}
        for row in available_times:
            room = row["rum_id"]
            tid = row["tid"]
            if room not in day_availability:
                day_availability[room] = []
            day_availability[room].append(tid)

        # Lägg till dagens tillgänglighet i veckans resultat
        week_availability[date_str] = day_availability

    conn.close()

    # Returnera resultatet
    if week_availability:
        return week_availability
>>>>>>> Stashed changes:app_dev.py
    else:
        raise HTTPException(status_code=404, detail="Inga lediga rum finns för denna vecka.")


# Endpoint för att boka ett rum
@app.post("/book-room")
async def book_room(data: BookingRequest):
    room_id = data.room_id
    tid = data.tid
    datum = data.datum

    # Validera tidens format och intervall
    if not validate_time_format(tid):
        raise HTTPException(status_code=422, detail="Ogiltigt tidsformat. Ange tiden i formatet HH:MM mellan 08:00 och 17:00.")

    # Validera datumformat och konvertera till datumobjekt
    try:
        booking_date = datetime.strptime(datum, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=422, detail="Ogiltigt datumformat. Ange datumet i formatet YYYY-MM-DD.")
    
    # Kontrollera att datumet inte är i det förflutna
    today = datetime.today().date()
    if booking_date < today:
        raise HTTPException(status_code=422, detail="Datumet ligger i det förflutna. Välj ett framtida datum.")
    
    # Kontrollera att datumet är en vardag (måndag-fredag)
    if booking_date.weekday() > 4:  # 0 = Måndag, 6 = Söndag
        raise HTTPException(status_code=422, detail="Endast bokningar mellan måndag och fredag är tillåtna.")

    # Förbered bokningen
    room = f"Room {room_id}"

    # Anslut till databasen och kontrollera om tiden är ledig
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE datum = ? AND rum_id = ?", (datum, f"Room {room_id}"))
    date_exists = cursor.fetchone()
    if not date_exists:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Datumet {datum} finns inte i databasen för rummet Room {room_id}.")

    # Om tiden är ledig, boka rummet
    if result and result["available"]:
        cursor.execute("UPDATE bookings SET available = 0 WHERE rum_id = ? AND datum = ? AND tid = ?", (room, datum, tid))
        conn.commit()
        conn.close()
        return {"message": f"Rummet {room} är nu bokat för {tid} den {datum}."}
    else:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Rummet {room} är redan bokat för {tid} den {datum}. Välj en annan tid.")
