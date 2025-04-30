import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE users (
        username TEXT NOT NULL PRIMARY KEY,
        password TEXT NOT NULL,
        src TEXT,
        dst TEXT,
        ride_completed INTEGER DEFAULT 0)
    
''')

conn.commit()
conn.close()