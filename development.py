#Databas

import sqlite3
from datetime import datetime, timedelta

#Funktion för att ansluta till databasen
def get_db_connection():
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Gör att vi kan använda kolumnnamn som nycklar
        return conn
    except sqlite3.Error as e:
        print(f'Ett fel uppstod vid anslutning till databasen: {e}')
        return None
    
def create_booking_table(conn):
    try:
        conn.execute('''
                    CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        room TEXT NOT NULL,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        available BOOLEAN DEFAULT 1
                    );
                ''')

    except sqlite3.Error as e:
            print(f'Ett fel uppstod när tabellen skulle skapas: {e}')

def populate_bookings():
    rooms = ['Room 1', 'Room 2', 'Room 3', 'Room 4', 'Room 5']
    start_time = 8  # 08:00
    end_time = 17   # 17:00
    tider = [f"{str(hour).zfill(2)}:00" for hour in range(start_time, end_time)]  # Time slots from 08:00 to 17:00

    today = datetime.today()
    weekdays = [today + timedelta(days=i) for i in range(7) if (today + timedelta(days=i)).weekday() < 5]  # Get this week's weekdays

    conn = get_db_connection()
    with conn:
        for room in rooms:
            for weekday in weekdays:
                for tid in tider:
                    # Insert available time slots into the database
                    conn.execute('INSERT INTO bookings (room, date, time, available) VALUES (?, ?, ?, ?)', 
                                 (room, weekday.date(), tid, True))
    conn.close()

              # Skapa tabell för rum
def create_rooms_table(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_name TEXT PRIMARY KEY
            );
        ''')
    except sqlite3.Error as e:
         print(f'Ett fel uppstod när tabellen rooms skulle skapas: {e}')
        # Lägg till fem tillgängliga rum om de inte redan finns

def initialize_database():
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn:
                create_booking_table(conn)
                create_rooms_table(conn)
            rooms = [('Room 1',), ('Room 2',), ('Room 3',), ('Room 4',), ('Room 5',)]
            conn.executemany('INSERT OR IGNORE INTO rooms (room_name) VALUES (?)', rooms)
        except sqlite3.Error as e:
            print(f'Ett fel uppstod under databasinitiering: {e}')
        finally:
            conn.close()
    else:
        print("Kunde inte ansluta till databasen")
#För att säkerställa att datum och tid följer korrekt format innan de sparas i databasen, 
#skapar vi en funktion som använder datetime för att validera och formatera datum och tid.
from datetime import datetime

def validate_and_format_date(date_str, time_str):
    try:
        # Kontrollera att datum är i formatet YYYY-MM-DD
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        # Kontrollera att tid är i formatet HH:MM
        time_obj = datetime.strptime(time_str, '%H:%M')

        # Returnera strängarna i rätt format om valideringen lyckas
        return date_obj.strftime('%Y-%m-%d'), time_obj.strftime('%H:%M')
    except ValueError as e:
        raise ValueError("Invalid date or time format. Expected 'YYYY-MM-DD' for date and 'HH:MM' for time.") from e

if __name__ == "__main__":
    initialize_database()
    print("Database initialized and table created (if not already present).")
