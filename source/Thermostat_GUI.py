import mysql.connector
from datetime import datetime, date
import time
import os
import sys
import threading
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT,Qt
from PyQt4.QtGui import *

set_mode=0

@pyqtSlot()
def coolOn():
    global set_mode
    if not cool.isChecked():
        #print('Cooling')
        set_mode = 1
        #print(set_mode)
        if heat.isChecked():
            heat.toggle()
    else:
        set_mode = 0
 
@pyqtSlot()
def heatOn():
    global set_mode
    if not heat.isChecked():
        #print('Heating')
        set_mode = -1
        if cool.isChecked():
            cool.toggle()
    else:
        set_mode = 0

@pyqtSlot()
def forceFan():
    global set_mode
    if not fan.isChecked():
        #print('Heating')
        set_mode = 3
    else:
        set_mode = 0

def increase_temp(self):

    global set_temp
    set_temp+=1
##        cursor = database.cursor()
##        try:
##            query = ("UPDATE status SET set_temp=set_temp+1 WHERE room = '{}' ".format(room))
##            cursor.execute(query)
##            database.commit()
##        except:
##            print('index')
##            w.deleteLater()
##            app.quit()
##        cursor.close()

def decrease_temp(self):
    global set_temp
    set_temp-=1
##        try:
##            query1 = ("UPDATE status SET set_temp=set_temp-1 WHERE room = '{}' ".format(room))
##            cursor1.execute(query1)
##            database.commit()
##        except:
##            print('index')
##            w.deleteLater()
##            app.quit()

def gui_run():
    global set_temp
    while True:
        if not( down.isDown() or up.isDown()):
            query2 = ("SELECT feel_temp,on_off,heat,cool,humidity FROM status WHERE room = '{}' ".format(room))
            try:
                cursor2.execute(query2)
                result=cursor2.fetchall()
            except:
                    print('error')
                    w.deleteLater()
                    app.quit()
            finally:
                database.commit()
                
        query2=("UPDATE status SET set_temp={}, on_off ={} WHERE room={}".format(set_temp,set_mode,room))
        cursor2.execute(query2)
        database.commit()

        real_temp = result[0][0]
        on_off = result[0][1]
        heat = result[0][2]
        cool = result[0][3]
        humidity = result[0][4]
##        set_temp = result[0][5]
        
        realt.setText('{0:0.1f}\xb0F'.format(real_temp))
        sett.setText('{0:0.0f}\xb0F'.format(set_temp))
        humDisp.setText('{0:0.1f}%'.format(humidity))
        time.sleep(0.5)


database= mysql.connector.connect(user='root', password='thermo',host='127.0.0.1',database='thermostat')


cursor1 = database.cursor()
cursor2 = database.cursor()
room =0

query2 = ("SELECT set_temp FROM status WHERE room = '{}' ".format(room))
cursor2.execute(query2)
result=cursor2.fetchall()
set_temp=result[0][0]
database.commit()

# create our window
app = QApplication(sys.argv)
w = QWidget()

coolPal=QPalette()
coolPal.setColor(QPalette.Active,QPalette.Window,QColor(111,195,214))
heatPal=QPalette()
heatPal.setColor(QPalette.Active,QPalette.Window,QColor(235,96,96))
offPal=QPalette()
offPal.setColor(QPalette.Active,QPalette.Window,QColor(255,255,255))
w.setPalette(offPal)

# Create buttons in the window
quitButton = QPushButton('X',w)
quitButton.pressed.connect(quit)
quitButton.setGeometry(0,0,15,15)

up = QToolButton(w)
up.setArrowType(1)
up.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

down = QToolButton(w)
down.setArrowType(2)
down.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

cool = QPushButton('Cool',w)
cool.setCheckable(True)
fan = QPushButton('Fan',w)
fan.setCheckable(True)
heat = QPushButton('Heat',w)
heat.setCheckable(True)

#create Labels
font = QFont("Times",25)

humDisp = QLabel(w)
humDisp.setAlignment(Qt.AlignCenter)
humDisp.setFont(font)

realt = QLabel(w)
realt.setAlignment(Qt.AlignCenter)
realt.setFont(font)

sett = QLabel(w)
sett.setAlignment(Qt.AlignCenter)
sett.setFont(font)

temps = QVBoxLayout()

temps.addWidget(realt)
temps.addWidget(humDisp)

buttons = QVBoxLayout()
buttons.addWidget(up)
buttons.addWidget(sett)
buttons.addWidget(down)

setting = QVBoxLayout()
setting.addWidget(cool)
setting.addWidget(fan)
setting.addWidget(heat)

hbox = QHBoxLayout()
hbox.addLayout(setting)
hbox.addLayout(temps)
hbox.addLayout(buttons)

# connect the signals to the slots
up.setAutoRepeat(True)
up.setAutoRepeatDelay(1000)
up.setAutoRepeatInterval(500)
down.setAutoRepeat(True)
down.setAutoRepeatDelay(1000)
down.setAutoRepeatInterval(500)
up.clicked.connect(increase_temp)
down.clicked.connect(decrease_temp)
print('hi')
cool.pressed.connect(coolOn)
fan.pressed.connect(forceFan)
heat.pressed.connect(heatOn)


w.setLayout(hbox)
w.setFixedSize(320,240)
w.showFullScreen()

thr2=threading.Thread(target = gui_run)
thr2.setDaemon(True)
thr2.start()





if __name__ == '__main__':
     try:
         sys.exit(app.exec_())
         print('help')

             
     finally:
        print('bye')
        cursor.close()
        database.close()
