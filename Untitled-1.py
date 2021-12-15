
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
main_df = pd.DataFrame(cursor.fetchall(), columns=['ids'])
client_ids = main_df['ids'].to_list()
rev_customers = []
customers_name = []
el_list = []
name_list=[]

for ids in client_ids:
    cursor.execute('SELECT username FROM Users WHERE id=?', [ids])
    customers_name.append(cursor.fetchone()[0])
    cursor.execute('SELECT quote_id FROM Quotes WHERE client_id=?', [ids])
    second_df = pd.DataFrame(cursor.fetchall(), columns=['Quotes ids'])
    quote_ids = second_df['Quotes ids'].to_list()
    print(quote_ids)
    if quote_ids:
        for qids in quote_ids:
            cursor.execute('SELECT subscriptions_list FROM Quotes WHERE quote_id=?', [qids])
            fetch_subs = json.loads(cursor.fetchone()[0])
            for elements in fetch_subs:
                cursor.execute('''
                    SELECT name
                    FROM Subscriptions
                    WHERE subscription_id=?
                ''', [elements])
                name = cursor.fetchone()[0]
                el_list.append(name)
        name_list.append(el_list)
    else:
        name_list.append("No subscription")

print(name_list)

main_df['Names'] = customers_name # columns names
main_df['Subscriptions'] = name_list #column subs
print(main_df)

#mean = sum(rev_customers) / len(rev_customers)
#return {"message": "The average revenue per customer is: {average_revenue}".format(average_revenue = mean)}

