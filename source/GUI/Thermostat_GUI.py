
#!/usr/bin/python
# Copyright (c) 2014 Mathew Jordan
# Author: Mathew Jordan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#import read_local_air as local_air
from queue import Queue
import mysql.connector
from datetime import datetime, date
import time
import os
import sys
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT,Qt
from PyQt4.QtGui import *

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

# Create a button in the window
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
#cool.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.MinimumExpanding)
heat = QPushButton('heat',w)
heat.setCheckable(True)
#heat.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.MinimumExpanding)

class QLCD(QLCDNumber):

    global number
 
    @pyqtSlot()
    def increaseValue(progressBar):
        global number
        number = number + 1
        progressBar.display(number)
        
        
    @pyqtSlot()
    def decreaseValue(progressBar):
        global number
        number = number - 1
        progressBar.display(number)
        


# Create Numbers. 
##sett = QLCD(w)   
##sett.display(desired_temp)
##sett.setFrameStyle(0)
##sett.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

#realt = QLCD(w)   
#realt.display(loc_feel)
#realt.setFrameStyle(0)



##humDisp = QLCD(w)
##humDisp.display(loc_hum)
##humDisp.setFrameStyle(0)

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



        #print('Temp = {0:0.2f} F'.format(loc_temp))
        #print('Feels = {0:0.2f} F'.format(loc_feel))
        #print('Humidity = {0:0.2f} %'.format(loc_hum))
        #print(' ')
        #print('Set Temp = {0:0.2f} %'.format(desired_temp))
        #print(fan_state)
        #sett.display(str(desired_temp)+'\'')
        #realt.display(str(int(loc_feel))+'\'')
global desired_temp
desired_temp = 10
realt.setText('{0:0.1f}\xb0F'.format(25))
sett.setText('{0:0.0f}\xb0F'.format(desired_temp))
humDisp.setText('{0:0.1f}%'.format(25))

#humDisp.display(loc_hum)
time.sleep(1)

def increase_temp(self):
       global desired_temp
       desired_temp += 1

def decrease_temp(self):
       global desired_temp
       desired_temp -= 1






 
# Create the actions 

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
    
 
# connect the signals to the slots
up.clicked.connect(increase_temp)
down.clicked.connect(decrease_temp)

cool.pressed.connect(coolOn)
heat.pressed.connect(heatOn)
 
# Show the window and run the app

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



w.setLayout(hbox)
w.setFixedSize(320,240)
#w.show()
w.showFullScreen()
app.exec_()

if __name__ == '__main__':
     try:
         while True:
             pass
     finally:
         pass
