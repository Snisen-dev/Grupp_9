#Databas

import sqlite3

#Funktion för att ansluta till databasen
def get_db_connection():
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Gör att vi kan använda kolumnnamn som nycklar
        return conn
    except sqlite3.Error as e:
        print(f'Ett fel uppstod vid anslutning till databasen: {e}')
        return None
    
#Skapar en funktion som ansluter till databasen och skapar tabellen "bookings" om den inte redan finns
def initialize_database():
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        room TEXT NOT NULL,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        avalaible BOOLEAN DEFAULT 1
                    );
                ''')
                
        except sqlite3.Error as e:
            print(f'Ett fel uppstod när tabellen skulle skapas: {e}')

              # Skapa tabell för rum
        conn.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                room_name TEXT PRIMARY KEY
            );
        ''')

        # Lägg till fem tillgängliga rum om de inte redan finns
        rooms = [('Room 1',), ('Room 2',), ('Room 3',), ('Room 4',), ('Room 5',)]
        conn.executemany('INSERT OR IGNORE INTO rooms (room_name) VALUES (?)', rooms)
    conn.close()

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
