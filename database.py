import sqlite3
from typing import List, Dict

# Funktion för att ansluta till databasen
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Gör så att vi kan använda kolumnnamn som nycklar
    return conn

# Initiera databasen och skapa tabellen om den inte finns
def initialize_database():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                booked BOOLEAN DEFAULT 1
            );
        ''')
    conn.close()

# Funktion för att boka ett rum
def book_room(room: str, date: str, time: str) -> bool:
    AVAILABLE_ROOMS = ['room1', 'room2', 'room3', 'room4', 'room5']
    if room not in AVAILABLE_ROOMS:
        return False  # Rummet finns inte i listan med tillgängliga rum

    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM bookings WHERE room = ? AND date = ? AND time = ?",
                (room, date, time)
            )
            if cursor.fetchone():
                return False  # Rummet är redan bokat vid den tiden

            conn.execute(
                "INSERT INTO bookings (room, date, time, booked) VALUES (?, ?, ?, ?)",
                (room, date, time, True)
            )
            return True
    except Exception as e:
        print(f"Error booking room: {e}")
        return False

# Funktion för att hämta alla bokningar
def get_bookings() -> List[Dict]:
    try:
        with get_db_connection() as conn:
            cursor = conn.execute("SELECT * FROM bookings")
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error retrieving bookings: {e}")
        return []
