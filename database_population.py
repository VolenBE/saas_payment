import sqlite3
import random

dbase = sqlite3.connect('database.db', isolation_level=None)
cursor = dbase.cursor()

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
    temp = random.sample(all,longueur) #take random elements from letters and numbers for a total set length
    password = "".join(temp) #put the sample that we get in a string
    return password

def random_number():
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    temp = random.sample(numbers, 8)
    bankaccount = "".join(temp)
    return bankaccount

def random_price():
    random_price = random.randint(5,100) 
    return random_price

def random_company_name():
    cursor.execute('SELECT company_name FROM Companies ORDER BY RANDOM() LIMIT 1') #we pick a random company from the db
    random_company_name = cursor.fetchone()[0]
    return random_company_name

def random_address():
    rue = ['des Marroniers', 'de la Thyria', 'Neuve', 'Roosevelt', 'des Monthys']
    ville = ['Bruxelles', 'Namur', 'Liège', 'Charleroi']
    all = str(random.choice(range(1,100))) + ' rue ' + random.choice(rue) + ', ' + random.choice(ville)
    return all

def select_random_companyid():
    cursor.execute('SELECT company_id FROM Companies ORDER BY RANDOM() LIMIT 1')
    chosen_companyid = cursor.fetchone()[0]
    return chosen_companyid

def random_client_id():
    cursor.execute('SELECT client_id FROM Clients ORDER BY RANDOM() LIMIT 1')
    chosen_id = cursor.fetchone()[0]
    return chosen_id

def create_company(username, password, bankaccount, address, vatid, company_name):
    cursor.execute(''' 
            INSERT INTO Users(username,password,bankaccount,address)
            VALUES(?,?,?,?)''', (username, password, bankaccount, address))
    print("Account successfully created")
    company_id = int(cursor.lastrowid)
    cursor.execute('''
        INSERT INTO Companies(company_id, vatid, company_name)
        VALUES(?,?,?)''', (company_id, vatid, company_name))

def populate_companies():
    for i in range(1, 15):
        username = "".join(random_username())
        name =  "".join(get_company_names())
        create_company(username, random_password(8), random_number(), random_address(), random_number(), name)
populate_companies()
def create_client(company_id, username, password, bankaccount, address):
    cursor.execute(''' 
        INSERT INTO Users(username,password,bankaccount,address)
        VALUES(?,?,?,?)''', (username, password, bankaccount, address))
    print("Customer account successfully created")
    client_id = int(cursor.lastrowid)
    cursor.execute('''
        INSERT INTO Clients(client_id, company_id)
        VALUES(?,?)''', (client_id,company_id))
    print("Client id added to the Clients table")

def populate_clients():
    for i in range(1, 15):
        username = "".join(random_username())
        create_client(select_random_companyid(), username, random_password(8), random_number(),random_address())
populate_clients()
def create_subscriptions(amount, client_id, name):
    cursor.execute('''
        INSERT INTO Subscriptions(name, client_id, status, price)
        VALUES(?,?,?,?)''', (name, client_id, 0, amount))

def populate_subscriptions():
    for i in range(1, 15):
        create_subscriptions(random_price(), random_client_id(), random_company_name())
populate_subscriptions()

def generate_quote_price():
    total_amount = 0
    currency = "EUR"
    cursor.execute('SELECT name, price_id FROM Subscriptions ORDER BY RANDOM() LIMIT 3')
    random_sub1 = cursor.fetchall()
    for i in range(0,len(random_sub1)):
        cursor.execute('SELECT amount_euro FROM Prices WHERE price_id=?', [random_sub1[i][1]])
        total_amount = total_amount + float(cursor.fetchone()[0])
    cursor.execute('''
        INSERT INTO Prices(amount, currency,amount_euro)
        VALUES(?,?,?)''', (total_amount,currency,total_amount))