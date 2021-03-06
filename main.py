import sqlite3
import json
import datetime
from datetime import date
import urllib.request
from fastapi import FastAPI, Request
import uvicorn
import pandas as pd

app = FastAPI()

@app.get("/")
def root():
  return {"message": "It works !"}


# Useful Functions


def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    lastday = next_month - datetime.timedelta(days=next_month.day)
    return lastday

  # source: https://stackoverflow.com/a/13565185/13466313

def checkCard(card_number):
  # we initialize the variable we will use during the iteration
  digits_sum = 0 
  card_number = [int(x) for x in str(card_number)] #we turn the int into an array to be able to use reversed()
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

#il faut faire une requete api pour chaque ??l??ment, ajout d'un client, d'une subscription, ...
#update les rates ?? chaque calcul
#AMR = argent re??u par mois par customers
#lorsque le customer paye l'invoice on stocke ?? ce moment l?? la currency utilis??e et on convertit le prix en euro dans la monnaie choisie
#faire en sorte que le statut de la invoice soit chang?? automatiquement le dernier jour du mois une fois
#peut ??tre stocker la dernier date de paiement genre if date = lastdayofthemonth && lastpaymentdate != lastdayofthemonth then:

@app.post("/register_client")
async def register_client(payload: Request):
    values_dict = await payload.json()
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
    dbase = sqlite3.connect('database.db', isolation_level=None)
    cursor = dbase.cursor()

    cursor.execute('''
        INSERT INTO Subscriptions(name,client_id,status,price)
        VALUES("{name}","{client_id}","{status}","{price}")'''.format(name = str(values_dict['name']),client_id=int(values_dict['client_id']),status=int(values_dict['status']),price=int(values_dict['price'])))
    return {"message": "Subscription successfuly created"}
# API request : Quote creation

@app.post("/quote_creation")
async def quote_creation(payload: Request):
    values_dict = await payload.json()
    dbase = sqlite3.connect('database.db', isolation_level=None)
    cursor = dbase.cursor()
    total_price = 0

    client_id = values_dict['client_id']
    company_id = values_dict['company_id']

    cursor.execute('SELECT client_id FROM Clients WHERE company_id=? AND client_id=?', [company_id, client_id])

    if cursor.fetchone() == None:
      return {"message": "The customer is not a client from the company"}
    
    # with more time would have added a check to make sure subscription is linked to the client before converting to quote

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
  dbase = sqlite3.connect('database.db', isolation_level=None)
  cursor = dbase.cursor()

  check_query = cursor.execute('''
    SELECT client_id, accepted, price_eur
    FROM Quotes
    WHERE quote_id={}
  '''.format(str(values_dict['quote_id'])))

  fetch = check_query.fetchone()

  id_client = fetch[0]
  status = fetch[1]
  amount = fetch[2]

  if id_client != values_dict['client_id'] or status != 1:
    return "Error"

  cursor.execute('''
    INSERT INTO Invoices(pending, client_id, quote_id, amount)
    VALUES("{pending}","{client_id}","{quote_id}", "{amount}")
  '''.format(pending=int(values_dict['pending']),client_id=int(values_dict['client_id']),quote_id=int(values_dict['quote_id']),amount=int(amount)))
  return {"message": "Successfully converted the quote !"}

# API request : Check if there is a pending invoice

@app.post("/invoice")
async def invoice(payload: Request):
  values_dict = await payload.json()
  dbase = sqlite3.connect('database.db', isolation_level=None)
  cursor = dbase.cursor()

  client_id = values_dict['client_id']

  pending_query = cursor.execute('''
    SELECT pending, quote_id
    FROM Invoices
    WHERE client_id=?
  ''', [client_id])

  fetch = pending_query.fetchone()

  if fetch != None and fetch[0] == 1:
    quote_id = fetch[1]
    quote_query = cursor.execute('''
      SELECT subscriptions_list, price_eur
      FROM Quotes
      WHERE quote_id=?
    ''', [quote_id])
    fetch_quote = quote_query.fetchone()

    subscriptions_list = json.loads(fetch_quote[0])
    name_list = []

    for elements in subscriptions_list:
      cursor.execute('''
        SELECT name
        FROM Subscriptions
        WHERE subscription_id=?
      ''', [elements])
      name = cursor.fetchone()[0]
      name_list.append(name)

    price = fetch_quote[1]

    name_list = ', '.join(name_list)

    return {"message": "You have a pending invoice concerning the following subscriptions: {subs} for a total price of: {pricet} euros".format(subs=name_list,pricet=int(price))}
  else:
    return {"message": "error"}
# API request : Pay invoice using credit card number

@app.post("/pay_invoice")
async def pay_invoice(payload: Request):
  values_dict = await payload.json()
  dbase = sqlite3.connect('database.db', isolation_level=None)
  cursor = dbase.cursor()

  card_number = int(values_dict['cardnumber'])
  invoice = int(values_dict['invoice_id'])
  currency = str(values_dict['currency'])
  client_id = int(values_dict['client_id'])

  first_query = cursor.execute('SELECT pending, quote_id FROM Invoices WHERE invoice_id=?', [invoice])
  fetch_first = first_query.fetchone()
  pending = fetch_first[0]
  quote_id = fetch_first[1]

  if pending == 1:
    second_query = cursor.execute('SELECT price_eur FROM Quotes WHERE quote_id=?', [quote_id])
    price_eur = second_query.fetchone()[0]
    rate = get_rate(currency)
    price = price_eur * rate

    if checkCard(card_number):
      pending_query = cursor.execute('''
        SELECT pending, quote_id
        FROM Invoices
        WHERE client_id=?
        ''', [client_id])

      fetch = pending_query.fetchone()
      print(fetch)
      quote_id = fetch[1]
      quote_query = cursor.execute('''
        SELECT subscriptions_list, price_eur
        FROM Quotes
        WHERE quote_id=?
      ''', [quote_id])
      fetch_quote = quote_query.fetchone()
      print(fetch_quote)

      subscriptions_list = json.loads(fetch_quote[0])

      for elements in subscriptions_list:
        cursor.execute('''
          UPDATE Subscriptions
          SET status=1
          WHERE subscription_id=?
        ''', [elements])

      cursor.execute('''
        INSERT INTO Payments(invoice_id, amount_eur, currency_name, amount_currency, success, LastPaymentDate)
        VALUES(?,?,?,?,?,?)
      ''', (invoice,price_eur,currency,price, 1, date.isoformat(datetime.datetime.now())))
      cursor.execute('UPDATE Invoices SET pending = 0 WHERE invoice_id=?', [invoice])
      return {"message": "Payment successful"}
    else:
      cursor.execute('''
        INSERT INTO Payments(invoice_id, amount_eur, currency_name, amount_currency, success, LastPaymentDate)
        VALUES(?,?,?,?,?,?)
      ''', (invoice,price_eur,currency,price, 0, date.isoformat(datetime.datetime.now())))

      pending_query = cursor.execute('''
        SELECT pending, quote_id
        FROM Invoices
        WHERE client_id=?
        ''', [client_id])

      fetch = pending_query.fetchone()

      quote_id = fetch[1]
      quote_query = cursor.execute('''
        SELECT subscriptions_list, price_eur
        FROM Quotes
        WHERE quote_id=?
      ''', [quote_id])
      fetch_quote = quote_query.fetchone()

      subscriptions_list = json.loads(fetch_quote[0])

      for elements in subscriptions_list:
        cursor.execute('''
          UPDATE Subscriptions
          SET status=2
          WHERE subscription_id=?
        ''', [elements])
      return {"message": "Payment unsuccessful"}
  else:
    return {"message": "Invoice already paid"}
  

# API request : Company retrieve their stats


#1.Monthly Recurring Revenue (MRR) which is the predictable total revenue generated
#by a company from all the active subscriptions in a particular month.

# for subscriptions status = 0, temp status that we give when creating  the quote, 1 active, 2 cancelled


@app.get("/mrr")
async def mrr(payload: Request):
  values_dict = await payload.json()
  dbase = sqlite3.connect('database.db', isolation_level=None)
  cursor = dbase.cursor()

  company_id = values_dict['company_id']

  cursor.execute('SELECT client_id FROM Clients WHERE company_id=?', [company_id])
  df_one = pd.DataFrame(cursor.fetchall(), columns=['ids'])
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
  MRR = sum(active) + sum(pending) - sum(canceled)

  return {"message": "Your MMR is: {MRR}".format(MRR=int(round(MRR, 2)))}
#Note we didn't consider the fact that there could be upgrade or downgrades so our MRR is way more "simplified here" MRR should normally be:
# Total amount from montly subs + total amount gained from new customers in month + total amount gained from upgrades and add ons in month - total amount lost from downgrades in motnh - total amount lost from churn


#2. Annual Recurring Revenue (ARR), which is the value of the recurring revenue of a
#business's term subscriptions normalized for a single calendar year. It is a
#subscription economy metric that shows the money that comes in every year for the
#life of a subscription (or contract).

@app.get("/arr")
async def arr(payload: Request):
  values_dict = await payload.json()
  dbase = sqlite3.connect('database.db', isolation_level=None)
  cursor = dbase.cursor()

  company_id = values_dict['company_id']

  cursor.execute('SELECT client_id FROM Clients WHERE company_id=?', [company_id])
  df_one = pd.DataFrame(cursor.fetchall(), columns=['ids'])

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
  MRR = sum(active) + sum(pending) - sum(canceled)
  ARR = MRR * 12
  return {"message": "Your ARR is: {ARR}".format(ARR=int(round(ARR, 2)))}

#3. Number of customers

@app.get("/number_customers")
async def number_customers(payload: Request):
  values_dict = await payload.json()
  dbase = sqlite3.connect('database.db', isolation_level=None)
  cursor = dbase.cursor()

  company_id = values_dict['company_id']

  # Number of customers
  cursor.execute('''
    SELECT COUNT()
    FROM Clients
    WHERE company_id=?  
  ''', [company_id])

  number_clients = cursor.fetchone()[0]

  return {"message": "You have a total of: {number_clients} customers".format(number_clients=number_clients)}


#4. Average revenues per customers


@app.get("/average_revenue")
async def average_revenue(payload: Request):
  values_dict = await payload.json()
  dbase = sqlite3.connect('database.db', isolation_level=None)
  cursor = dbase.cursor()

  company_id = values_dict['company_id']

  cursor.execute('SELECT client_id FROM Clients WHERE company_id=?', [company_id])
  df = pd.DataFrame(cursor.fetchall(), columns=['ids'])
  client_ids = df['ids'].to_list()
  rev_customers = []

  for ids in client_ids:
    cursor.execute('SELECT invoice_id, amount FROM Invoices WHERE client_id=?', [ids])
    fetch = cursor.fetchone()
    if fetch != None:
        invoice_id = fetch[0]
        amount = fetch[1]
        rev_customers.append(amount)
  mean = sum(rev_customers) / len(rev_customers)
  return {"message": "The average revenue per customer is: {average_revenue}".format(average_revenue = mean)}
  
#5. A table of all customers with their current subscriptions

@app.get("/customer_subs")
async def customer_subs(payload: Request):
  values_dict = await payload.json()
  dbase = sqlite3.connect('database.db', isolation_level=None)
  cursor = dbase.cursor()

  company_id = values_dict['company_id']
  
  cursor.execute('SELECT client_id FROM Clients WHERE company_id=?', [company_id])
  main_df = pd.DataFrame(cursor.fetchall(), columns=['ids'])
  client_ids = main_df['ids'].to_list()
  customers_name = []
  el_list = []
  name_list=[]

  for ids in client_ids:
      cursor.execute('SELECT username FROM Users WHERE id=?', [ids])
      customers_name.append(cursor.fetchone()[0])
      cursor.execute('SELECT quote_id FROM Quotes WHERE client_id=?', [ids])
      second_df = pd.DataFrame(cursor.fetchall(), columns=['Quotes ids'])
      quote_ids = second_df['Quotes ids'].to_list()

      if quote_ids: #si l'array n'est pas vide
          for qids in quote_ids: # on r??alise une itteration sur les diff??rents quote id
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
      else: #si l'array est vide
          name_list.append("No subscription")

  main_df['Names'] = customers_name # columns names
  main_df['Subscriptions'] = name_list #column subs
  print(main_df)

# Server launch and reset invoices if last day of the month 

if __name__ == '__main__':
  dbase = sqlite3.connect('database.db', isolation_level=None)
  cursor = dbase.cursor()
  lastday = last_day_of_month(datetime.datetime.now()) #we get the last day of this month

  result = lastday.day - datetime.datetime.now().day #we substract last day of the month with the actual one
  cursor.execute('SELECT LastReset FROM Tech')
  fetch = cursor.fetchone()
  if fetch == None:
      cursor.execute('INSERT INTO Tech(LastReset) VALUES(?)', [datetime.datetime.now()])
  last_reset = datetime.datetime.strptime(fetch[0], '%Y-%m-%d %H:%M:%S.%f') #we need to convert back the str stored in the database to a timestamp
  diff_reset = last_day_of_month(datetime.datetime.now()).day - last_reset.day #we check that last reset wasn't today

  if result == 0 and diff_reset != 0:
    cursor.execute('SELECT COUNT() FROM Invoices')
    fetch = 1 + cursor.fetchone()[0] # +1 to counter python stopping before reaching the end of the range
    for i in range(1, fetch):
      cursor.execute('UPDATE Invoices SET pending = 1 WHERE invoice_id = ?', [i])
    cursor.execute('UPDATE Tech SET LastReset=?', [datetime.datetime.now()])
    
  uvicorn.run(app, host='127.0.0.1', port=8000)



