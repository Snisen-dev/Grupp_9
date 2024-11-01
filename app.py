from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict
from database import get_db_connection, validate_and_format_date
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {'Message': 'Välkommen till Grupp 9:s bokningssystem'}

@app.get("/rooms", response_model=List[Dict[str, str]])
async def check_bookings():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, room, date, time, avalaible
            FROM bookings
            ORDER BY date, room, time
        """)
        bookings = cursor.fetchall()
        conn.close()

        return [
            {
                "id": str(booking["id"]),
                "room": booking["room"],
                "date": booking["date"],
                "time": booking["time"],
                "available": "Yes" if booking["avalaible"] else "No"
            }
            for booking in bookings
        ]
    except Exception as e:
        logger.error(f"Error in check_bookings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/rooms/booked", response_model=List[Dict[str, str]])
async def booked_rooms(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    try:
        validated_date, _ = validate_and_format_date(date, "00:00")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT room, time
            FROM bookings 
            WHERE date = ? AND avalaible = 0
            ORDER BY room, time
        """, (validated_date,))
        booked = cursor.fetchall()
        conn.close()

        return [dict(room) for room in booked]
    except Exception as e:
        logger.error(f"Error in booked_rooms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/rooms/unbooked", response_model=List[Dict[str, str]])
async def unbooked_rooms(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    try:
        validated_date, _ = validate_and_format_date(date, "00:00")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE date = ?", (validated_date,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            conn.close()
            return [{"message": f"No bookings found for date {validated_date}"}]
        
        cursor.execute("""
            SELECT room, time
            FROM bookings 
            WHERE date = ? AND avalaible = 1
            ORDER BY room, time
        """, (validated_date,))
        unbooked = cursor.fetchall()
        conn.close()

        if not unbooked:
            return [{"message": f"All rooms are booked for date {validated_date}"}]

        return [dict(room) for room in unbooked]
    except Exception as e:
        logger.error(f"Error in unbooked_rooms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/book")
async def new_booking(room: str, date: str, time: str):
    try:
        validated_date, validated_time = validate_and_format_date(date, time)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT avalaible
            FROM bookings
            WHERE room = ? AND date = ? AND time = ?
        """, (room, validated_date, validated_time))
        result = cursor.fetchone()

        if result is None:
            cursor.execute("""
                INSERT INTO bookings (room, date, time, avalaible)
                VALUES (?, ?, ?, 0)
            """, (room, validated_date, validated_time))
        elif result['avalaible'] == 1:
            cursor.execute("""
                UPDATE bookings
                SET avalaible = 0
                WHERE room = ? AND date = ? AND time = ?
            """, (room, validated_date, validated_time))
        else:
            raise HTTPException(status_code=400, detail="Room is already booked")

        conn.commit()
        return {"message": f"Room {room} booked successfully for {validated_date} at {validated_time}"}
    except Exception as e:
        conn.rollback()
        logger.error(f"Error in new_booking: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)