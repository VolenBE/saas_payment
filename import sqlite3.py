import sqlite3

dbase = sqlite3.connect('database.db', isolation_level=None)
cursor = dbase.cursor()

element = 2

check_query = cursor.execute('''
    SELECT client_id, accepted
    FROM Quotes
    WHERE quote_id=?
  ''', [element])
fetch = check_query.fetchone()

id_client = fetch[0]
status = fetch[1]


print(id_client, status)