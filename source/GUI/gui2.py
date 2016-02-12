import mysql.connector
from datetime import datetime, date
import time
import os
import sys
import threading
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT,Qt
from PyQt4.QtGui import *

@pyqtSlot()
def coolOn():
    global set_mode
    if not cool.isChecked():
        #print('Cooling')
        set_mode = COOL_MODE
        #print(set_mode)
        if heat.isChecked():
            heat.toggle()
    else:
        set_mode = OFF_MODE
 
@pyqtSlot()
def heatOn():
    global set_mode
    if not heat.isChecked():
        #print('Heating')
        set_mode = HEAT_MODE
        if cool.isChecked():
            cool.toggle()
    else:
        set_mode = OFF_MODE

def increase_temp(self):
       global desired_temp
       desired_temp += 1

def decrease_temp(self):
       global desired_temp
       desired_temp -= 1

def gui_run():
    while True:
        query = ("SELECT feel_temp,on_off,heat,cool,humidity FROM status WHERE room = '{}' ".format(room))
        cursor.execute(query)
        result=cursor.fetchall()
        database.commit()

        real_temp = result[0][0]
        on_off = result[0][1]
        heat = result[0][2]
        cool = result[0][3]
        humidity = result[0][4]
        
        realt.setText('{0:0.1f}\xb0F'.format(real_temp))
        sett.setText('{0:0.0f}\xb0F'.format(15))
        humDisp.setText('{0:0.1f}%'.format(humidity))



database= mysql.connector.connect(user='root', password='thermo',host='127.0.0.1',database='thermostat')

cursor = database.cursor()

room =0

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

heat = QPushButton('heat',w)
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
setting.addWidget(heat)

hbox = QHBoxLayout()
hbox.addLayout(setting)
hbox.addLayout(temps)
hbox.addLayout(buttons)

# connect the signals to the slots
up.clicked.connect(increase_temp)
down.clicked.connect(decrease_temp)
print('hi')
cool.pressed.connect(coolOn)
heat.pressed.connect(heatOn)


w.setLayout(hbox)
w.setFixedSize(320,240)
w.showFullScreen()

thr2=threading.Thread(target = gui_run)
thr2.setDaemon(True)
thr2.start()

app.exec_()


if __name__ == '__main__':
     try:
         while True:
             pass
             
     finally:
        print('bye')
        cursor.close()
        database.close()
