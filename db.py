# We will use the SQLite database
import sqlite3

# Initialize database connection and cursor
con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Create table "Subscription" with uid and balance rows
cur.execute('''CREATE TABLE IF NOT EXISTS Users(
                uid STRING,
                addr STRING
        )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Owners(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                addr STRING
        )''')

for i in range(0, 221):
    cur.execute(f'INSERT INTO Owners (addr) VALUES ("0x123")')

def update_owner(wallet_address, id):
    cur.execute(f'UPDATE Owners SET addr = "{wallet_address}" where id = {id}')
    con.commit()

def add_user(uid):
    cur.execute(f'INSERT INTO Users VALUES ({uid}, "0x123")')
    con.commit()

def check_user(uid):
    cur.execute(f'SELECT * FROM Users WHERE uid = {uid}')
    user = cur.fetchone()
    if user:
        return True
    return add_user(uid)

def remove_user(uid):
    cur.execute(f'DELETE FROM Users WHERE uid = {uid}')
    con.commit()

def unbond_address(uid):
    cur.execute(f'UPDATE Users SET addr = "0x00" WHERE uid = {uid}')
    con.commit()

def check_address(wallet_address):
    cur.execute(f'SELECT * FROM Users WHERE addr = "{wallet_address}"')
    duplicated = cur.fetchone()
    if duplicated:
        return unbond_address(duplicated[0])
    return True

def set_address(uid, wallet_address):
    check_address(wallet_address)
    cur.execute(f'UPDATE Users SET addr = "{wallet_address}" WHERE uid = {uid}')
    con.commit()