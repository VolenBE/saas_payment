import sqlite3

dbase = sqlite3.connect('database.db', isolation_level=None)
print('Database opened')
dbase.execute("PRAGMA foreign_keys = 1")

#Users

dbase.execute(''' CREATE TABLE IF NOT EXISTS Users
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username VARCHAR(64) NOT NULL,
        password VARCHAR(64) NOT NULL,
        bankaccount INT NOT NULL,
        address VARCHAR(128) NOT NULL
    )''')
print("Table user created successfully")

#Companies

dbase.execute(''' CREATE TABLE IF NOT EXISTS Companies
    (
        company_id INT,
        vatid INT NOT NULL,
        company_name VARCHAR NOT NULL,
        FOREIGN KEY (company_id) REFERENCES Users(ID)
    )''')
print("Table Companies created successfully")

#Clients

dbase.execute(''' CREATE TABLE IF NOT EXISTS Clients
    (
        client_id INT NOT NULL,
        company_id INT NOT NULL,
        FOREIGN KEY (company_id) REFERENCES Companies(company_id),
        FOREIGN KEY (client_id) REFERENCES Users(id)
    )''')
print("Table Clients created successfully")

#Analytics

dbase.execute(''' CREATE TABLE IF NOT EXISTS Analytics
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        MRR INT NOT NULL,
        AAR INT NOT NULL,
        number_customers INT NOT NULL,
        average_revenue INT NOT NULL,
        company_id INT NOT NULL,
        FOREIGN KEY (company_id) REFERENCES Companies(company_id)
    )''')
print("Table Analytics created successfully")

#Prices

#dbase.execute(''' CREATE TABLE IF NOT EXISTS Prices
    #(
     #   price_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #    amount INT NOT NULL,
   #     currency VARCHAR(64) NOT NULL,
  #      amount_euro INT NOT NULL
 #   )''')
#print("Table Prices created successfully")

#Quotes

dbase.execute(''' CREATE TABLE IF NOT EXISTS Quotes
    (
        quote_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        company_id INT NOT NULL,
        client_id INT NOT NULL,
        quantity INT NOT NULL,
        subscriptions_list VARCHAR(248),
        price_eur INT NOT NULL,
        accepted BOOLEAN,
        FOREIGN KEY (company_id) REFERENCES Companies(company_id),
        FOREIGN KEY (client_id) REFERENCES Clients(client_id)
    )''')
print("Table Quotes created successfully")

#Invoices

dbase.execute(''' CREATE TABLE IF NOT EXISTS Invoices
    (
        invoice_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        pending BOOLEAN,
        client_id INT NOT NULL,
        quote_id INT NOT NULL,
        amount INT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients(client_id),
        FOREIGN KEY (quote_id) REFERENCES Quotes(quote_id)
    )''')
print("Table Invoices created successfully")

#Payments

dbase.execute(''' CREATE TABLE IF NOT EXISTS Payments
    (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        invoice_id INT NOT NULL,
        amount_eur INT NOT NULL,
        currency_name char(3) NOT NULL,
        amount_currency INT NOT NULL,
        success BOOLEAN NOT NULL,
        LastPaymentDate TIMESTAMP,
        FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id)
    )''')
print("Table Payments created successfully")

#Subscriptions

dbase.execute(''' CREATE TABLE IF NOT EXISTS Subscriptions
    (
        subscription_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name VARCHAR(64),
        client_id INT NOT NULL,
        status INT NOT NULL,
        price INT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES Clients(client_id)
    )''')
print("Table Subscriptions created successfully")

# Currencies

dbase.execute('''CREATE TABLE IF NOT EXISTS Currencies
    (
        currency_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        rate INT NOT NULL
    )
''')
print("Table Currencies created successfully")

# Technical

dbase.execute('''CREATE TABLE IF NOT EXISTS Tech
    (
        LastReset TIMESTAMP
    )
''')
print("Table Tech created successfully")


#dbase.execute(''' 
#                INSERT INTO Users(username,password,bankaccount,address)
#                VALUES('antoine','antoine',1023891,'avenue louise 12')
#''')

dbase.close()
print('Database Closed')