
import sqlite3
import json
import datetime
from datetime import date
import urllib.request
from fastapi import FastAPI, Request
import uvicorn
import pandas as pd



# Useful Functions
dbase = sqlite3.connect('database.db', isolation_level=None)
cursor = dbase.cursor()

company_id = 10

cursor.execute('SELECT client_id FROM Clients WHERE company_id=?', [company_id])
df = pd.DataFrame(cursor.fetchall(), columns=['ids'])
client_ids = df['ids'].to_list()
print(client_ids)
rev_customers = []

for ids in client_ids:
    cursor.execute('SELECT invoice_id, amount FROM Invoices WHERE client_id=?', [ids])
    fetch = cursor.fetchone()
    if fetch != None:
        invoice_id = fetch[0]
        amount = fetch[1]
        rev_customers.append(amount)

math = sum(rev_customers) / len(rev_customers)
print(math)

