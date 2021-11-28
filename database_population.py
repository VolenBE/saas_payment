import sqlite3
import json

dbase = sqlite3.connect('database.db', isolation_level=None)
cursor = dbase.cursor()

def create_client(company_id, username, password, bankaccount, address):

    cursor.execute(''' 
        INSERT INTO Users(username,password,bankaccount,address)
        VALUES(?,?,?,?)''', (username, password, bankaccount, address))
    print("Customer account successfully created")
    client_id = int(cursor.lastrowid)
    print(client_id)
    cursor.execute(''' 
        INSERT INTO Clients(client_id)
        VALUES(?)''', (client_id,))
    print("Client id added to the Clients table")
    sclient_id = json.dumps(client_id)
    cursor.execute('UPDATE Companies set client_ids_list='+ sclient_id +' WHERE ID=' + company_id)
    print("Client added to the clients ids list")

def create_company(username, password, bankaccount, address, vatid, company_name):
    cursor.execute(''' 
            INSERT INTO Users(username,password,bankaccount,address)
            VALUES(?,?,?,?)''', (username, password, bankaccount, address))
    print("Account successfully created")
    company_id = int(cursor.lastrowid)
    print(company_id)
    cursor.execute('''
        INSERT INTO Companies(company_id, vatid, company_name)
        VALUES(?,?,?,?)''', (company_id, vatid, company_name))

def create_subscriptions(amount, currency, name):
    amount_euro = amount / currency
    cursor.execute('''
        INSERT INTO Prices(amount, currency,amount_euro)
        VALUES(?,?,?)''', (amount,currency,amount_euro))
    #we get the row id we just created
    new_price_id = int(cursor.lastrowid)
    #we now create a new row into subscriptions
    cursor.execute('''
        INSERT INTO Subscriptions(name, active, price_id)
        VALUES(?,?,?)''', (name, 0, new_price_id))
