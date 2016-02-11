
# Copyright (c) 2016 Mathew Jordan
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
import mysql.connector


def apparent_temp(t,RH):
    Tf=t*1.8+32
    if Tf >= 70 and RH >= 40:
        app_temp = -42.379+2.04901523*(Tf)+10.14333127*(RH)-0.22475541*(Tf)*(RH)-6.83783*10**(-3)*(Tf**(2))-5.481717*10**(-2)*(RH**(2))+1.22874*10**(-3)*(Tf**(2))*(RH)+8.5282*10**(-4)*(Tf)*(RH**(2))-1.99*10**(-6)*(Tf**(2))*(RH**(2))
    else:
        app_temp = Tf
    return app_temp

database= mysql.connector.connect(user='root', password='thermo',host='127.0.0.1',database='thermostat')
cursor = database.cursor()

def read():
    local = local_air.read_local_air()
    local_temp_c = local[0]
    local_temp_f = local_temp_c*1.8+32
    local_hum = local[1]
    local_press = local[2]/100.0
    local_feel_f =apparent_temp(local[0],local[1])
    local_temp = local_temp_f

    query = "UPDATE status SET temp = {},humidity = {},feel_temp = {},pressure = {} where room = 0".format(local_temp_f,local_hum,local_feel_f,local_press)
    cursor.execute(query)
    database.commit()

    

    
if __name__ == '__main__':
    try:
        while True:
            read()
             
    finally:
        cursor.close()
        database.close()
