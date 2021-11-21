import sqlite3
import getpass # might be useless in this case

# Initialize variables

logged_in = 0

# Functions

def checkCard(card_number):
     
    digits = len(card_number)
    sum_numbers = 0
    isSecond = False
     
    for i in range(digits - 1, -1, -1):
        d = ord(card_number[i]) - ord('0')
     
        if (isSecond == True):
            d = d * 2
  
        # We add two digits to handle
        # cases that make two digits after
        # doubling
        sum_numbers += d // 10
        sum_numbers += d % 10
  
        isSecond = not isSecond
     
    if (sum_numbers % 10 == 0):
        return True
    else:
        return False

# we ask the user about his/her details, we should add a check to know if the user is a company or a client

username = input('Your username:')
userpass = getpass.getpass('Your password:')

# Establish a connection to the database

dbase = sqlite3.connect('database.db', isolation_level=None)
cursor = dbase.cursor()

cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, userpass)) # we make a sql request to see if there is a matching record

if cursor.fetchall():
    print('Welcome', username) # if there is a matching record we welcome the user
    logged_in = 1
else:
    print("Sorry it seems we can't find you in our database") #if there is no matching record we tell the user
    register = int(input("Would you like to register? If so please type 1"))
    if register == 1:
        wanted_username = input('Please choose a username:')
        wanted_password = input('Please choose a password:')
        bankaccount = input('Bank account:')
        address = input('Address:')
        vatid = input('Your vat id:')
        company_name = input('Your company name:')
        dbase.execute(''' 
            INSERT INTO Users(username,password,bankaccount,address)
            VALUES(?,?,?,?)''', (wanted_username, wanted_password, bankaccount, address))
        print("Account successfully created")
    else:
        print('Bye bye')

if logged_in == 1:
    actions = int(input("Please tell us what would you like to do: \n Type 1 to register a new Customer \n Type 2 to create a quote \n Type 3 to convert a quote into a subscription \n Type 4 to retrieve statistics"))
    if actions == 1:
        customer_username = input('Please choose a username for your customer:')
        customer_password = input('Please choose a password for your customer:')
        customer_bankaccount = input('Please provide your customer bank account number:')
        customer_address = input('Please provide your customer address:')
        cursor.execute(''' 
            INSERT INTO Users(username,password,bankaccount,address)
            VALUES(?,?,?,?)''', (customer_username, customer_password, customer_bankaccount, customer_address))
        print("Customer account successfully created")
        temp_id = int(cursor.lastrowid)
        print(temp_id)
        cursor.execute(''' 
            INSERT INTO Clients(client_id)
            VALUES(?)''', (temp_id,))
        print("Client id added to the Clients table")
    elif actions == 2:
        print('2')
    elif actions == 3:
        print('3')
    elif actions == 4:
        print('4')
else:
    exit()




