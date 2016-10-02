#logging

file = open('../../thermo_log.csv','w')

import mysql.connector
import time
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
        
        file.write(str(set_temp))
        file.write(',')
        file.write(str(real_temp))
        file.write(',')
        file.write(str(humidity))
        file.write(';')
        time.sleep(10)
