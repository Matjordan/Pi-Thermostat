
import mysql.connector
import RPi.GPIO as GPIO
import time


HEATER_PIN = 26
FAN_PIN = 20
COMP_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(HEATER_PIN, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.setup(COMP_PIN, GPIO.OUT)

database= mysql.connector.connect(user='root', password='thermo',host='127.0.0.1',database='thermostat')

cursor = database.cursor()

room =0

def run():

    query = ("SELECT on_off,fan,heat,cool FROM status WHERE room = '{}' ".format(room))
    cursor.execute(query)
    result=cursor.fetchall()
    database.commit()
    on_off = result[0][0]
    fan = result[0][1]
    heat = result[0][2]
    cool = result[0][3]
    
    if cool:
        GPIO.output(COMP_PIN, True)
    else:
        GPIO.output(COMP_PIN, False)

    if heat:
        GPIO.output(HEATER_PIN, True)
    else:
        GPIO.output(HEATER_PIN, False)

    if fan:
        GPIO.output(FAN_PIN, True)
    else:
        GPIO.output(FAN_PIN, False)
        

if __name__ == '__main__':
     try:
         while True:
             run()
             time.sleep(1)
     finally:
        print('bye')
        GPIO.cleanup()
        cursor.close()
        database.close()
