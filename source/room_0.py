
import mysql.connector
from datetime import date, datetime, timedelta,time

database= mysql.connector.connect(user='root', password='thermo',host='127.0.0.1',database='thermostat')

cursor = database.cursor()
today=date.today()
hour=datetime.today().hour
room=0 #default room

query = ("SELECT t{}00 FROM room_{} WHERE day = '{}' ".format(hour,room,today))
cursor.execute(query)
result=cursor.fetchall()

if None in result[0]:
    query = ("SELECT def_temp FROM room_{} WHERE day = '{}' ".format(room,today))
    cursor.execute(query)
    result=cursor.fetchall()
    
set_temp = result[0][0]

query = ("SELECT feel_temp,on_off,heat,cool FROM status WHERE room = '{}' ".format(room))
cursor.execute(query)
result=cursor.fetchall()

real_temp = result[0][0]
on_off = result[0][1]
heat = result[0][2]
cool = result[0][3]
print(set_temp)
print(real_temp)
print(on_off)
if on_off>0:
    if (real_temp > set_temp+1) and cool==0:
        cool=1
        heat=0
    if (real_temp < set_temp-2) and cool==1:
        cool=0
        heat=0
elif on_off<0:
    if (real_temp < set_temp-1) and heat==0:
        cool=0
        heat=1
    if (real_temp > set_temp+2) and heat==1:
        cool=0
        heat=0
else:
    heat=0
    cool=0
fan=1 #default room fan always on
vent=100 #default room vent always open

query = "UPDATE status SET set_temp = {},vent = {},fan = {},heat = {},cool ={} where room = {}".format(set_temp,vent,fan,heat,cool,room)
cursor.execute(query)
database.commit()

cursor.close()
database.close()