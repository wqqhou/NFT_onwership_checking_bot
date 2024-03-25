# We will use the SQLite database
import sqlite3

# Initialize database connection and cursor
con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Create table "Subscription" with uid and balance rows
cur.execute('''CREATE TABLE IF NOT EXISTS Users(
                uid STRING,
                address STRING
        )''')

def add_user(uid):
    cur.execute(f'INSERT INTO Users VALUES ({uid}, "0x00")')
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
    cur.execute(f'UPDATE Users SET address = "0x00" WHERE uid = {uid}')
    con.commit()

def check_address(address):
    cur.execute(f'SELECT * FROM Users WHERE address LIKE {address}')
    duplicated = cur.fetchone()
    if duplicated:
        return unbond_address(duplicated[0])
    return False

def set_address(uid, address):
    check_address(address)
    cur.execute(f'UPDATE Users SET address = {address} WHERE uid = {uid}')
    con.commit()