
import mysql.connector
from datetime import date, datetime, timedelta,time

database= mysql.connector.connect(user='root', password='thermo',host='127.0.0.1',database='thermostat')

cursor = database.cursor()
today=date(2016,1,1)
hour=datetime.today().hour

