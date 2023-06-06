#!/usr/bin/env python3
import serial


def check(moist_alarm):
    if moist_alarm < 20:
        return True
    else:
        return False


def alarm_function():
    # The serial port and baud rate
    port = '/dev/ttyACM2'
    baudrate = 115200
    #open the port
    sl = serial.Serial(port, baudrate)
    dat = sl.readline().decode().strip()
    #split values 
    var = dat.split(',')
    moist_alarm = float(var[2])
    moisture = check(moist_alarm)
    return moisture


if __name__ == '__main__':
    moisture_current = alarm_function()
    print(moisture_current)

    
        
            
