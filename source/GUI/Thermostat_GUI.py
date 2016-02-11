
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

import read_local_air as local_air
from queue import Queue
import RPi.GPIO as GPIO
import threading
import time
import os
import sys
from PyQt5.QtCore import pyqtSlot,SIGNAL,SLOT,Qt
from PyQt5.QtGui import *

ON = 1
OFF = 0

OFF_MODE = 0
COOL_MODE = 1
HEAT_MODE = 2

global desired_temp
desired_temp = 80

COLD_THRESH = -2.0
COOL_THRESH = -1.0
WARM_THRESH = 1.0
HOT_THRESH = 2.0

COLD = -2
COOL = -1
NORMAL = 0
WARM = 1
HOT = 2

COMP_OFF_TIME_THRESH = 15 * 60 #15 mins
FAN_ON_TIME_THRESH = 2 * 60 #2 mins

global ac_state 
ac_state = OFF
global fan_state
fan_state = OFF
global comp_state
comp_state = OFF
global heat_state
heat_state = OFF

global HEATER_PIN
HEATER_PIN = 26
global FAN_PIN
FAN_PIN = 20
global COMP_PIN
COMP_PIN = 21


#global set_mode
set_mode = OFF_MODE
#global loc_temp
loc_temp = 0
#global loc_feel
loc_feel = 0
#global loc_hum
loc_hum = 0
#global loc_press
loc_press = 0

read_ready=threading.Event()

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

def cls():
    os.system(['clear','cls'][os.name == 'nt'])


def apparent_temp(t,RH):
	Tf=t*1.8+32

	app_temp = -42.379+2.04901523*(Tf)+10.14333127*(RH)-0.22475541*(Tf)*(RH)-6.83783*10**(-3)*(Tf**(2))-5.481717*10**(-2)*(RH**(2))+1.22874*10**(-3)*(Tf**(2))*(RH)+8.5282*10**(-4)*(Tf)*(RH**(2))-1.99*10**(-6)*(Tf**(2))*(RH**(2))

	return app_temp



class temp_control(threading.Thread):

    def __init__(self,event):
        threading.Thread.__init__(self)
        self.daemon = True
        self.event=event
        
        global ac_state
        ac_state = OFF
        global fan_state
        fan_state = OFF
        global comp_state
        comp_state = OFF


    def run(self):
        global loc_temp
        global loc_hum
        global loc_feel
        global loc_press
        global desired_temp

        comp_on_time = 0
        comp_off_time = 0
        fan_on_time = 0
        fan_off_time = 0

        global ac_state
        global fan_state
        global comp_state
        global heat_state
        
        global FAN_PIN
        global COMP_PIN
        global HEATER_PIN

        while True:
            

            local = local_air.read_local_air()
            local_temp_c = local[0]
#            local_temp_c += -2
            local_temp_f = local_temp_c*1.8+32
            local_hum = local[1]
            local_press = local[2]
            local_feel_f =apparent_temp(local[0],local[1])
            local_temp = local_temp_f
                        
            set_temp_f=desired_temp
            
            loc_temp = local_temp_f
            loc_hum = local_hum
            loc_feel = local_feel_f
            loc_press = local_press            
            self.event.set()

            error_temp = local_temp - set_temp_f

            fuzz_temp = NORMAL
            if error_temp < COOL_THRESH:
                    fuzz_temp = COOL
            if error_temp < COLD_THRESH:
                    fuzz_temp = COLD
            if error_temp > WARM_THRESH:
                    fuzz_temp = WARM
            if error_temp > HOT_THRESH:
                    fuzz_temp = HOT
                 
            if fan_state is ON:
                    fan_on_time += 1
            if fan_state is OFF:
                    fan_off_time += 1
            if comp_state is ON:
                    comp_on_time += 1
            if comp_state is OFF:
                    comp_off_time += 1

            if fan_state is ON:
                GPIO.output(FAN_PIN, True)
            else:
                GPIO.output(FAN_PIN, False)
            if comp_state is ON:
                GPIO.output(COMP_PIN, True)
            else:
                GPIO.output(COMP_PIN, False)

            if set_mode is COOL_MODE:
                w.setPalette(coolPal)
            
                if ac_state is ON:
                        if comp_state is ON:
                                if fuzz_temp is COLD:
                                        comp_state = OFF
                                        comp_off_time = 0
                                if fuzz_temp is COOL:
                                        comp_state = OFF
                                        comp_off_time = 0
                                        fan_state = OFF
                                        fan_off_time = 0
                                        ac_state = OFF
                        if comp_state is OFF:
                                if fan_on_time > FAN_ON_TIME_THRESH:
                                        if local_temp + 0.5 < fan_start_temp:
                                                fan_start_temp = local_temp
                                                fan_on_time = 0
                                                if fuzz_temp is COOL or fuzz_temp is COLD:
                                                        fan_state = OFF
                                                        fan_off_time = 0
                                                        ac_state = OFF
                                        else:
                                                comp_state = ON
                                                comp_on_time = 0
                                if fuzz_temp is HOT:
                                        comp_state = ON
                                        comp_on_time = 0
                                if fuzz_temp is COOL or fuzz_temp is COLD:
                                        fan_state = OFF
                                        fan_on_time = 0
                else:
                        if fuzz_temp is WARM:
                                if comp_off_time < COMP_OFF_TIME_THRESH:
                                        ac_state = ON
                                        fan_state = ON
                                        fan_start_temp = local_temp
                                        fan_on_time = 0 
                                else:
                                        ac_state = ON
                                        fan_state = ON
                                        fan_on_time = 0
                                        comp_state = ON
                                        comp_on_time = 0
                        if fuzz_temp is HOT:
                                ac_state = ON
                                fan_state = ON
                                fan_on_time = 0
                                comp_state = ON
                                comp_on_time = 0
            if set_mode is HEAT_MODE:
                #heater
                #print(set_mode)
                w.setPalette(heatPal)
            if (set_mode is not 2) and (set_mode is not COOL_MODE):
                w.setPalette(offPal)
                fan_state = OFF
                comp_state = OFF
                ac_state = OFF
                heat_state = OFF
                
#            #print(ac_state)
#            #print(fan_state,fan_on_time,fan_off_time)
#            #print(comp_state,comp_on_time,comp_off_time)
#            time.sleep(1)

def prints():
    while True:
 #       f=read_ready.wait()
 #       read_ready.clear()
        #cls()
#        global desired_temp_f
        global loc_temp
        global loc_feel
        global loc_hum
        global loc_press
        global fan_state

        #print('Temp = {0:0.2f} F'.format(loc_temp))
        #print('Feels = {0:0.2f} F'.format(loc_feel))
        #print('Humidity = {0:0.2f} %'.format(loc_hum))
        #print(' ')
        #print('Set Temp = {0:0.2f} %'.format(desired_temp))
        #print(fan_state)
        #sett.display(str(desired_temp)+'\'')
        #realt.display(str(int(loc_feel))+'\'')
        realt.setText('{0:0.1f}\xb0F'.format(loc_feel))
        sett.setText('{0:0.0f}\xb0F'.format(desired_temp))
        humDisp.setText('{0:0.1f}%'.format(loc_hum))

        #humDisp.display(loc_hum)
        time.sleep(1)

def increase_temp(self):
       global desired_temp
       desired_temp += 1

def decrease_temp(self):
       global desired_temp
       desired_temp -= 1



GPIO.setmode(GPIO.BCM)


GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(HEATER_PIN, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.setup(COMP_PIN, GPIO.OUT)

GPIO.add_event_detect(17, GPIO.FALLING, callback=increase_temp, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=decrease_temp, bouncetime=300)

thr=temp_control(read_ready)
thr.setDaemon(True)
thr.start()
time.sleep(2)
thr2=threading.Thread(target = prints)
thr2.setDaemon(True)
thr2.start()


 
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
         GPIO.cleanup()
	
	

