import sqlite3
from datetime import datetime,timedelta


# Funktion för att ansluta till databasen
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Gör att vi kan använda kolumnnamn som nycklar
    return conn

#Skapar en funktion som ansluter till databasen och skapar tabellen "bookings" om den inte redan finns
def initialize_database():
    conn = get_db_connection()
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
    conn.close()

def populate_bookings():
    rooms = ["Room 1 ", "Room 2 ", "Room 3 ", "Room 4 ", "Room 5 "]
    start_time = 8  # 08:00
    end_time = 17   # 17:00
    tider = [f" {str(hour).zfill(2)}:00 " for hour in range(start_time, end_time)]  # Tider från 08:00 till 16:00

    today = datetime.today()
    weekdays = [today + timedelta(days=i) for i in range(7) if (today + timedelta(days=i)).weekday() < 5]  # Veckans vardagar
    conn = get_db_connection()
    with conn:
        for room in rooms:
            for weekday in weekdays:
                for tid in tider:
                    # Infoga tillgängliga tider i databasen
                    date = weekday.date().isoformat() #Blir av med felmeddelandet  DeprecationWarning: The default date adapter is deprecated as of Python 3.12; see the sqlite3 documentation for suggested replacement recipes

                    conn.execute('INSERT INTO bookings (room, date, time, avalaible) VALUES (?, ?, ?, ?)', 
                                 (room, date, tid, True))
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


