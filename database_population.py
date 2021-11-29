import sqlite3
import requests
import json
import urllib.request
import random

dbase = sqlite3.connect('database.db', isolation_level=None)
cursor = dbase.cursor()

# A few functions to generate random elements

def get_company_names():
    company_names = []
    file = open('company_names.txt', 'r')
    content = file.readlines()

    for i in range(len(content)):
        company_names.append(content[i].splitlines())
    file.close()
    chosen = random.choice(company_names)
    company_names.remove(chosen)
    return chosen
def random_username():
    usernames = []
    file = open('usernames.txt', 'r')
    content = file.readlines()

    for i in range(len(content)):
        usernames.append(content[i].splitlines())
    file.close()
    chosen = random.choice(usernames)
    usernames.remove(chosen)
    return chosen

def random_password(longueur):
    letters = ['A','B','D','e','F','z','m','i']
    numbers = ['1','2','3','4','5','6','7','8','9']
    all = letters + numbers
    temp = random.sample(all,longueur)
    password = "".join(temp)
    return password

def random_number():
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    temp = random.sample(numbers, 8)
    bankaccount = "".join(temp)
    return bankaccount

def random_address():
    rue = ['des Marroniers', 'de la Thyria', 'Neuve', 'Roosevelt', 'des Monthys']
    ville = ['Bruxelles', 'Namur', 'Liège', 'Charleroi']
    all = str(random.choice(range(1,100))) + ' rue ' + random.choice(rue) + ', ' + random.choice(ville)
    return all

def select_random_companyid():
    #we use the ORDER BY RANDOM() to avoid writing python for this
    cursor.execute('SELECT company_id FROM Companies ORDER BY RANDOM() LIMIT 1')
    chosen_companyid = cursor.fetchone()[0]
    return chosen_companyid

# function create company

def create_company(username, password, bankaccount, address, vatid, company_name):
    cursor.execute(''' 
            INSERT INTO Users(username,password,bankaccount,address)
            VALUES(?,?,?,?)''', (username, password, bankaccount, address))
    print("Account successfully created")
    company_id = int(cursor.lastrowid)
    cursor.execute('''
        INSERT INTO Companies(company_id, vatid, company_name)
        VALUES(?,?,?)''', (company_id, vatid, company_name))

# populate company table
def populate_companies():
    for i in range(1, 15):
        i = 1
        username = "".join(random_username())
        name =  "".join(get_company_names())
        create_company(username, random_password(8), random_number(), random_address(), random_number(), name)
        i = i + 1

populate_companies()
# function create client

def create_client(company_id, username, password, bankaccount, address):
    cursor.execute(''' 
        INSERT INTO Users(username,password,bankaccount,address)
        VALUES(?,?,?,?)''', (username, password, bankaccount, address))
    print("Customer account successfully created")
    client_id = int(cursor.lastrowid)
    print(client_id)
    cursor.execute('''
        INSERT INTO Clients(client_id, company_id)
        VALUES(?,?)''', (client_id,company_id))
    print("Client id added to the Clients table")

#populate clients
def populate_clients():
    username = "".join(random_username())
    for i in range(1, 15):
        i=1
        create_client(select_random_companyid(), username, random_password(8), random_number(),random_address())
        i=i+1
populate_clients()

def create_subscriptions(amount, currency, name):
    cursor.execute('SELECT rate FROM Currencies WHERE name=?', [currency])
    rate = float(cursor.fetchone()[0])
    print(rate)
    amount_euro = amount / rate
    print(amount_euro)
    cursor.execute('''
        INSERT INTO Prices(amount, currency,amount_euro)
        VALUES(?,?,?)''', (amount,currency,amount_euro))
    #we get the row id we just created
    new_price_id = int(cursor.lastrowid)
    #we now create a new row into subscriptions
    cursor.execute('''
        INSERT INTO Subscriptions(name, active, price_id)
        VALUES(?,?,?)''', (name, 0, new_price_id))
#create_subscriptions(16, 'USD', 'spotify')
def get_rates():
    url = 'https://v6.exchangerate-api.com/v6/0108a9426d9afb4ab050af15/latest/EUR'
    data = urllib.request.urlopen(url).read().decode()
    
    obj = json.loads(data)

    for currency, rate in obj['conversion_rates'].items():
        cursor.execute('INSERT INTO Currencies(name,rate) VALUES(?,?)', (currency, rate))

def update_rates():
    url = 'https://v6.exchangerate-api.com/v6/0108a9426d9afb4ab050af15/latest/EUR'
    data = urllib.request.urlopen(url).read().decode()
    
    obj = json.loads(data)

    for currency, rate in obj['conversion_rates'].items():
        cursor.execute('UPDATE Currencies SET rate=? WHERE name=?', (rate, currency))
