import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
#             ('adeoyevictor', 'Cheekzy16@')
#             )

# cur.execute("INSERT INTO posts (user, title, content) VALUES (?, ?, ?)",
#             (1, 'First Post', 'Content for the first post')
#             )

# cur.execute("INSERT INTO posts (user, title, content) VALUES (?, ?, ?)",
#             (1, 'Second Post', 'Content for the second post')
#             )

connection.commit()
connection.close()