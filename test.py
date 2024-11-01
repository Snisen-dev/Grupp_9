import sqlite3

def initialize_database():
    conn = sqlite3.connect('database.db')
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

# Initiera databasen för att säkerställa att tabellen skapas
initialize_database()

# Anslut till databasen
conn = sqlite3.connect('database.db')
cursor = conn.execute("SELECT * FROM bookings")  
for row in cursor.fetchall():
    print(row)  
conn.close()  
