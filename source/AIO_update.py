import mysql.connector
from Adafruit_IO import Client
import time
aio= Client('9d7181cd2a41458a8ad55d5ea88215c5')
database= mysql.connector.connect(user='root', password='thermo',host='127.0.0.1',database='thermostat')

cursor = database.cursor()
room = 0
while True:
        query = ("SELECT temp,on_off,heat,cool,humidity,set_temp FROM status WHERE room = '{}' ".format(room))
        cursor.execute(query)
        result=cursor.fetchall()
        database.commit()

        real_temp = result[0][0]
        on_off = result[0][1]
        heat = result[0][2]
        cool = result[0][3]
        humidity = result[0][4]
        set_temp = result[0][5]
        
        data=aio.receive('set temp')
        
        remote_set_temp=float(data.value)
#        query = ("UPDATE status SET set_temp = '{}' WHERE room = 0".format(remote_set_temp))
#        cursor.execute(query)
#        database.commit()
	
#        set_temp=remote_set_temp
        aio.send('real temp',real_temp)
        aio.send('set temp',set_temp)
        aio.send('humidity',humidity)
        time.sleep(10)

