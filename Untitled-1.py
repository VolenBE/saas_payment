
import datetime
from datetime import date



# Useful Functions


def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    lastday = next_month - datetime.timedelta(days=next_month.day)
    return lastday

lastday = last_day_of_month(datetime.datetime.now())

result = lastday.day - datetime.datetime.now().day

print(result)

