import sqlite3

conn = sqlite3.connect("app/database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM requests")
rows = cursor.fetchall()

for row in rows:
    print(dict(zip([column[0] for column in cursor.description], row)))

conn.close()
