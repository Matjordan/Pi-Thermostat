
import mysql.connector
from datetime import date, datetime
import time

database= mysql.connector.connect(user='root', password='thermo',host='127.0.0.1',database='thermostat')
cursor = database.cursor()

def run():
    today=date.today()
    hour=datetime.today().hour
    room=0 #default room

    query = ("SELECT override FROM status WHERE room = '{}' ".format(room))
    cursor.execute(query)
    result=cursor.fetchall()
    override=result[0][0]

    if override==1: #manual temporary override of temp 
        
        query = ("SELECT set_temp FROM status WHERE room = '{}' ".format(room))
        cursor.execute(query)
        result=cursor.fetchall()
        set_temp=result[0][0]
    elif override == 0: #no override of temp using database
        query = ("SELECT t{}00 FROM room_{} WHERE day = '{}' ".format(hour,room,today))
        cursor.execute(query)
        result=cursor.fetchall()

        if None in result[0]:
            query = ("SELECT def_temp FROM room_{} WHERE day = '{}' ".format(room,today))
            cursor.execute(query)
            result=cursor.fetchall()
            
        set_temp = result[0][0]
        query = ("UPDATE status SET set_temp={} WHERE room = '{}' ".format(set_temp,room))
        cursor.execute(query)
        result=cursor.fetchall()
        database.commit()
        



    query = ("SELECT feel_temp,on_off,heat,cool FROM status WHERE room = '{}' ".format(room))
    cursor.execute(query)
    result=cursor.fetchall()
    
    database.commit()
    
    real_temp = result[0][0]
    on_off = result[0][1]
    heat = result[0][2]
    cool = result[0][3]

    if on_off==1:
        heat=0
        if (real_temp > set_temp+1) and cool==0:
            cool=1
        if (real_temp < set_temp-1):
            cool=0
    elif on_off==-1:
        cool=0
        if (real_temp < set_temp-1) and heat==0:
            heat=1
        if (real_temp > set_temp+1):
            heat=0
    elif on_off==2: #override for cool always on
        cool=1
        heat=0
    elif on_off==-2: #override for cool always on
        cool=0
        heat=1
    elif on_off==3: #override for fan
        cool=0
        heat=0
        fan=1
    else:
        heat=0
        cool=0
        fan=0
        
    if (heat or cool) and on_off < 3:
        fan=1
    elif on_off < 3:
        fan=0
        
    vent=100 #default room vent always open

    query = "UPDATE status SET vent = {},fan = {},heat = {},cool ={} where room = {}".format(vent,fan,heat,cool,room)
    cursor.execute(query)
    database.commit()

if __name__ == '__main__':
    try:
        while True:
            run()
            time.sleep(1)
             
    finally:
        cursor.close()
        database.close()


