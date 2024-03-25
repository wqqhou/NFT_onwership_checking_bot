# We will use the SQLite database
import sqlite3

# Initialize database connection and cursor
con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Create table "Subscription" with uid and balance rows
cur.execute('''CREATE TABLE IF NOT EXISTS Subscription(
                uid STRING
        )''')

def get_subscribers():
    cur.execute(f'SELECT * FROM Subscription')
    data = cur.fetchone()[0]
    uid_list = eval(data)
    if uid_list:
        return uid_list
    return False

def add_subscriber(uid):
    list = get_subscribers()
    list.append(str(uid))
    list = str(list)
    cur.execute(f'UPDATE Subscription SET uid = "{list}"')
    con.commit()

def check_subscriber(uid):
    list = get_subscribers()
    uid = str(uid)
    if list:
        if uid in list:
            return True
    return False

def remove_subscriber(uid):
    list = get_subscribers()
    uid = str(uid)
    if list:
        if uid in list:
            list.remove(uid)
            cur.execute(f'UPDATE Subscription SET uid = "{list}"')
            con.commit()
            return True
    return False