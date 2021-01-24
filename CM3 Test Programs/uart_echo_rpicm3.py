import serial
from time import sleep

s1 = serial.Serial ("/dev/ttyS0", 9600) #open port with given baud rate (9600, 38400, etc.)
while True:
    received_data = s1.read() #read serial port
    sleep (0.03)
    data_left = s1.inWaiting() #check for remaining byte
    received_data += s1.read(data_left)
    print (received_data) #print received data
    s1.write(received_data) #transmit data serially