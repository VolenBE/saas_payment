import sqlite3
import json
import requests
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

# First API request : Quote creation

@app.post("/quote_creation")
async def quote_creation(payload: Request):
    values_dict = await payload.json()
    # Open the DB
    dbase = sqlite3.connect('database.db', isolation_level=None)
    cursor = dbase.cursor()
    # Step 1: we create the query

    creation_query = cursor.execute('''
                    INSERT INTO Quotes(company_id,client_id,quantity,price_id,subscriptions_list,accepted)
                    VALUES({company_id},{client_id},{quantity},{price_id},{subscriptions_list},{accepted})

    ''')

    return True

def get_rates():
    request = requests.get('https://v6.exchangerate-api.com/v6/0108a9426d9afb4ab050af15/latest/EUR')
    print(request.json()['conversion_rates'])

print(get_rates())

@app.post("/accepting_quote")
async def accepting_quote():
  # We will put here the code to execute
  return True

@app.post("/convert_quote")
async def convert_quote():
  # We will put here the code to execute
  return True

@app.post("/invoice")
async def invoice():
  # We will put here the code to execute
  return True

@app.post("/pay_invoice")
async def pay_invoice():
  # We will put here the code to execute
  return True

@app.post("/retrieve_stats")
async def retrieve_stats():
  # We will put here the code to execute
  return True






