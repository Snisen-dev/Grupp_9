import sqlite3
from datetime import datetime, timedelta
import os

# Funktion för att ansluta till databasen
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Gör att vi kan använda kolumnnamn som nycklar
    return conn

# Funktion för att skapa tabellen "bookings" om den inte redan finns
def initialize_database():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                available BOOLEAN DEFAULT 1
            );
        ''')
    conn.close()

# Funktion för att fylla tabellen med bokningsbara tider
def populate_bookings():
    rooms = ["Room 1", "Room 2", "Room 3", "Room 4", "Room 5"]
    start_time = 8  # 08:00
    end_time = 17   # 17:00
    tider = [f"{str(hour).zfill(2)}:00" for hour in range(start_time, end_time)]

    today = datetime.today()
    weekdays = [today + timedelta(days=i) for i in range(7) if (today + timedelta(days=i)).weekday() < 5]
    
    conn = get_db_connection()
    with conn:
        for room in rooms:
            for weekday in weekdays:
                for tid in tider:
                    date = weekday.date().isoformat()
                    conn.execute('INSERT INTO bookings (room, date, time, available) VALUES (?, ?, ?, ?)', 
                                 (room, date, tid, True))
    conn.close()

if __name__ == "__main__":
    # Ta bort databasen om den redan finns för att skapa en ny med korrekt struktur
    if os.path.exists("database.db"):
        os.remove("database.db")
    
    initialize_database()
    populate_bookings()
    print("Database initialized and table created with available bookings.")
