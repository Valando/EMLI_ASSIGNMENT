
import machine
import time

uart = machine.UART(0, baudrate=115200)  

def send_request(char):
    uart.write(char.encode()) 

send_request('p')

