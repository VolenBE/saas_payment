
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


company_id = 3

cursor.execute('SELECT client_id FROM Clients WHERE company_id=?', [company_id])
df_one = pd.DataFrame(cursor.fetchall(), columns=['ids'])
print(df_one)
client_ids = df_one['ids'].to_list()
active = []
canceled = []
pending=[]

for ids in client_ids:
    cursor.execute('SELECT status, price FROM Subscriptions WHERE client_id=?', [ids])
    df_two = pd.DataFrame(cursor.fetchall(), columns=['Status','Price'])
    if not df_two.empty:
        active.append(df_two[df_two["Status"] == 1]["Price"].sum())
        canceled.append(df_two[df_two["Status"] == 2]["Price"].sum())
    cursor.execute('SELECT amount FROM Invoices WHERE pending=1 AND client_id=?', [ids])
    df_three = pd.DataFrame(cursor.fetchall(), columns=['Amount'])
    if not df_three.empty:
        pending.append(df_three['Amount'].sum())

#Note we didn't consider the fact that there could be upgrade or downgrades so our MRR is way more "simplified here" MRR should normally be:
# Total amount from montly subs + total amount gained from new customers in month + total amount gained from upgrades and add ons in month - total amount lost from downgrades in motnh - total amount lost from churn

MRR = sum(active) + sum(pending) - sum(canceled)
print(MRR)

        


