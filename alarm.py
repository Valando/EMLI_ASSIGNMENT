import serial


def check(plant_alarm, water_alarm):
    if plant_alarm or water_alarm:
        return True
    else:
        return False


def alarm_function():
    # The serial port and baud rate
    port = '/dev/ttyACM1'
    baudrate = 115200
    #open the port
    sl = serial.Serial(port, baudrate)
    dat = sl.readline().decode().strip()
    #split values 
    var = dat.split(',')
    plant_alarm = bool(int(var[0]))
    water_alarm = bool(int(var[1]))
    alarm = check(plant_alarm, water_alarm)
    return alarm


if __name__ == '__main__':
    alarm_current = alarm_function()
    print(alarm_current)

#yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyooooooooooooooooooooooooooooooooooooooooooooooyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyo
#yooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo    
