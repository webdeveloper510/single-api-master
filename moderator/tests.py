from django.test import TestCase

# Create your tests here.


import calendar
import datetime
now = datetime.datetime.now()

from calendar import Calendar

obj = calendar.Calendar()

days = []

for day in obj.itermonthdates(now.year, now.month):
    if day.month == now.month:
        days.append(day)
print(days)

