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

    def get_booked_rooms(self) -> List[Dict]:
        return [room.to_dict() for room in self.rooms if room.booked]

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
    else:
        raise HTTPException(status_code=400, detail="Room could not be booked. It is either already booked or doesn't exist.")