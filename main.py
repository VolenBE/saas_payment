import sqlite3
import json
import urllib.request
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.get("/")
def root():
  return {"message": "It works !"}


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

def get_rate(selected_currency):
    url = 'https://v6.exchangerate-api.com/v6/0108a9426d9afb4ab050af15/latest/EUR'
    data = urllib.request.urlopen(url).read().decode()
    
    obj = json.loads(data)

    for currency, rate in obj['conversion_rates'].items():
        if currency == selected_currency:
            selected_rate = rate
            return rate

#il faut faire une requete api pour chaque élément, ajout d'un client, d'une subscription, ...
#update les rates à chaque calcul
#AMR = argent reçu par mois par customers
#changer le système, stocker le prix de chaque subscriptions en euros dans la bdd, lorsque l'on crée la quote on stocke le prix total
#lorsque le customer paye l'invoice on stocke à ce moment là la currency utilisée et on convertit le prix en euro dans la monnaie choisie
#faire en sorte que le statut de la invoice soit changé automatiquement le dernier jour du mois une fois
#peut être stocker la dernier date de paiement genre if date = lastdayofthemonth && lastpaymentdate != lastdayofthemonth then:

@app.post("/register_client")
async def register_client(payload: Request):
    values_dict = await payload.json()
    # Open the DB
    dbase = sqlite3.connect('database.db', isolation_level=None)
    cursor = dbase.cursor()

    cursor.execute(''' 
      INSERT INTO Users(username,password,bankaccount,address)
      VALUES("{username}","{password}","{bankaccount}","{address}")
      '''.format(username=str(values_dict['username']), password=str(values_dict['password']), bankaccount=int(values_dict['bankaccount']), address=str(values_dict['address'])))
    client_id = int(cursor.lastrowid)
    cursor.execute('''
      INSERT INTO Clients(client_id, company_id)
      VALUES(?,?)''', (client_id,values_dict['company_id']))
    return {"message": "Successfully registered the client!"}

# API request: Subscription creation

@app.post("/subscription_creation")
async def subscription_creation(payload: Request):
    values_dict = await payload.json()
    # Open the DB
    dbase = sqlite3.connect('database.db', isolation_level=None)
    cursor = dbase.cursor()

    cursor.execute('''
        INSERT INTO Subscriptions(name, active, price)
        VALUES("{name}","{active}","{price}")'''.format(name = str(values_dict['name']),active=int(values_dict['active']), price=int(values_dict['price'])))

# API request : Quote creation

@app.post("/quote_creation")
async def quote_creation(payload: Request):
    values_dict = await payload.json()
    # Open the DB
    dbase = sqlite3.connect('database.db', isolation_level=None)
    cursor = dbase.cursor()
    total_price = 0
    
    subscriptions_list = json.loads(values_dict['subscriptions'])
    print(subscriptions_list)

    for subscriptions in subscriptions_list:
      cursor.execute('SELECT price FROM Subscriptions WHERE subscription_id=?', [subscriptions])
      total_price += int(cursor.fetchone()[0])

    cursor.execute('''
      INSERT INTO Quotes(company_id,client_id,quantity,price_eur,subscriptions_list,accepted)
      VALUES("{company_id}","{client_id}","{quantity}","{price}","{subscriptions}","{accepted}")
    '''.format(company_id=int(values_dict['company_id']),client_id=int(values_dict['client_id']),quantity=int(values_dict['quantity']),price=int(total_price),subscriptions=str(values_dict["subscriptions"]),accepted=int(values_dict['accepted'])))
    return {"message": "Successfully created the quote !"}

# API request : Quote acceptation from the client

@app.post("/accepting_quote")
async def accepting_quote(payload: Request):
  values_dict = await payload.json()
  # Open the DB
  dbase = sqlite3.connect('database.db', isolation_level=None)
  cursor = dbase.cursor()

  check_query = cursor.execute('''
    SELECT client_id, accepted
    FROM Quotes
    WHERE quote_id={}
  '''.format(str(values_dict['quote_id'])))

  id_client = check_query.fetchone()[0]

  print(id_client)

  if id_client != values_dict['client_id']:
    return "Error"

  cursor.execute('''
    UPDATE Quotes 
    SET accepted = {accepted}
    WHERE quote_id = {quote_id}
    AND client_id = {client_id}
    '''.format(accepted = int(values_dict['accepted']), quote_id = int(values_dict['quote_id']), client_id = int(values_dict['client_id'])))
  return {"message": "Successfully accepted the quote !"}

# API request : Quote convertion from the Company

@app.post("/convert_quote")
async def convert_quote(payload: Request):
  values_dict = await payload.json()
  # Open the DB; 
  dbase = sqlite3.connect('database.db', isolation_level=None)
  cursor = dbase.cursor()

  check_query = cursor.execute('''
    SELECT client_id, accepted
    FROM Quotes
    WHERE quote_id={}
  '''.format(str(values_dict['quote_id'])))

  fetch = check_query.fetchone()

  id_client = fetch[0]
  status = fetch[1]

  if id_client != values_dict['client_id'] or status != 1:
    return "Error"

  cursor.execute('''
    INSERT INTO Invoices(pending, client_id, quote_id)
    VALUES("{pending}","{client_id}","{quote_id}")
  '''.format(pending=int(values_dict['pending']),client_id=int(values_dict['client_id']),quote_id=int(values_dict['quote_id'])))
  return True

# API request : Check if there is a pending invoice

@app.get("/invoice")
async def invoice():
  # We will put here the code to execute
  return True

# API request : Pay invoice using credit card number

@app.post("/pay_invoice")
async def pay_invoice():
  # We will put here the code to execute
  return True

# API request : Company retrieve their stats

@app.get("/retrieve_stats")
async def retrieve_stats():
  # We will put here the code to execute
  return True


if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000)



