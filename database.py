import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Gör att vi kan använda kolumnnamn som nycklar
    return conn

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