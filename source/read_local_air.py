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

import Adafruit_BMP.BMP085 as BMP085
import time
import os
import HTU21D

def read_local_air():
	calOffSet = -3.5
	htu =HTU21D.HTU21D()
	bmp = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

	bmp_temp = bmp.read_temperature()
	htu_temp = htu.read_temperature()

	humidity = htu.read_humidity()
	baro_press = bmp.read_pressure()

	ave_temp = ((bmp_temp+htu_temp)/2.0) + calOffSet
	
	result = []
	result.append(ave_temp)
	result.append(humidity)
	result.append(baro_press)
	
	return result
def print_local_air():
	print(read_local_air())

if __name__ == "__main__":
    import sys
    print_local_air()	
