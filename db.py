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

def add_user(uid):
    cur.execute(f'INSERT INTO Users VALUES ({uid}, "0x123")')
    con.commit()

def check_user(uid):
    cur.execute(f'SELECT * FROM Users WHERE uid = {uid}')
    user = cur.fetchone()
    if user:
        return True
    return add_user(uid)

def get_addresses():
    cur.execute('SELECT addr FROM Users')
    return cur.fetchall()

def find_user(wallet_address):
    cur.execute(f'SELECT uid FROM Users WHERE addr = "{wallet_address}"')
    return cur.fetchone()

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