import sqlite3
import getpass # might be useless in this case
import json

# Initialize variables

logged_in = 0

# Functions

def checkCard(card_number):
     # we initialize the variable we will use during the iteration
    digits_sum = 0 

    #we use enumerate to get the count of the current iteration and the value of the item at the current iteration. Reversed is used to reverse the card_number since we are supposed to start from the end
    for i, digit in enumerate(reversed(card_number)): 
        #we make sure digit is an int 
        j = int(digit)  
        # we use the modulus operator to see if the number is dividable by 2
        if i % 2 == 0: 
            # if so we add it to the sum
            digits_sum += j 
        elif j >= 5: 
            # for the last numbers we multiply them by 2 and we subtract 9
            digits_sum += j * 2 - 9
        else: 
            # for the rest we just multiply them by 2
            digits_sum += j * 2
    # if the final sum is dividable by 10 we return true because the card number is valid 
    if  digits_sum % 10 == 0: 
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
    logged_in = 1
    cursor.execute('SELECT ID FROM Users WHERE username = ?', (username,)) # we get the id of the client 
    logged_id = cursor.fetchone()
    print(logged_id[0])
    cursor.execute('SELECT * FROM Companies WHERE company_id = ?', (logged_id[0]))
    if cursor.fetchall():
        print('Welcome', username, 'you are a Company') # if there is a matching record we welcome the user
        user_status = 1
    else:
        print('Welcome', username, 'you are a client')
        user_status = 2
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
        cursor.execute(''' 
            INSERT INTO Users(username,password,bankaccount,address)
            VALUES(?,?,?,?)''', (wanted_username, wanted_password, bankaccount, address))
        print("Account successfully created")
        company_id = int(cursor.lastrowid)
        print(company_id)
        cursor.execute('''
            INSERT INTO Companies(company_id, vatid, company_name)
            VALUES(?,?,?,?)''', (company_id, vatid, company_name))
    else:
        print('Bye bye')

if logged_in == 1 and user_status == 1:
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
        client_id = int(cursor.lastrowid)
        print(client_id)
        cursor.execute(''' 
            INSERT INTO Clients(client_id)
            VALUES(?)''', (client_id,))
        print("Client id added to the Clients table")
        sclient_id = json.dumps(client_id)
        cursor.execute('''
            INSERT INTO Companies(client_ids_list)
            VALUES(?)''', (sclient_id))
        print("Client added to the clients ids list")
    elif actions == 2:
        quote_client_id = input('Please type your client id:')
        quote_quantity = input('Please choose the quantity:')
        quote_price_id = input('Please specify the price_id:')
        cursor.execute('SELECT subscription_id, name FROM Subscriptions')
        print(cursor.fetchall())
        quote_subscriptions_list = input('Please list the subscriptions ids, if you want to create a new subscription please type "New":')
        if quote_subscriptions_list == "New":
            new_subscription_name = input("Please choose a name for your subscription: ")
            new_subscription_amount = int(input("Please enter the amount: "))
            new_subscription_currency = input("Please specify the currency: ")
            #first we add a row into the Prices table
            #at the moment we don't have the currency convertion module
            cursor.execute('''
                INSERT INTO Prices(amount, currency,amount_euro)
                VALUES(?,?,?)''', (new_subscription_amount,new_subscription_currency,new_subscription_amount))
            #we get the row id we just created
            new_price_id = int(cursor.lastrowid)
            #we now create a new row into subscriptions
            cursor.execute('''
                INSERT INTO Subscriptions(name, active, price_id)
                VALUES(?,?,?)''', (new_subscription_name, 0, new_price_id))
        quote_accepted = 0
        cursor.execute('''
            INSERT INTO Quotes(company_id, client_id, quantity, price_id, subscriptions_list, accepted)
            VALUES(?,?,?,?,?,?)''', (logged_id[0], quote_client_id, quote_quantity, quote_price_id, quote_subscriptions_list, quote_accepted))
    elif actions == 3:
        quote_tobechecked = input('Which quote would you like to check?')
        cursor.execute('SELECT accepted FROM Quotes WHERE quote_id = ?', (quote_tobechecked,))
        quote_status = cursor.fetchone()
        cursor.execute('SELECT subscriptions_list FROM Quotes WHERE quote_id = ?', (quote_tobechecked,))
        subscriptions_list = cursor.fetchall()
        if quote_status[0] == 1:
            print("Your quote has been accepted by your client we're going to turn it into an active subscription")
            for subscriptions in subscriptions_list:
                cursor.execute('''
                INSERT INTO Subscriptions(name, active)
                VALUES(?,?)''', (subscriptions, 1))
        else:
            print("Your quote hasn't been accepted by your client yet")
    elif actions == 4:
        print('4')
elif logged_in == 1 and user_status == 2:
    action_user = int(input('Please choose one of the following actions \n Type 1 to check if you want to see pending quotes \n Type 2 to check pending invoices \n Type 3 to exit'))
    if action_user == 1:
        print('1')
    elif action_user == 2:
        print('2')
    elif action_user == 3:
        print('3')
else:
    exit()





