import serial



class DriveController:
    def __init__(self, device, baudrate):
        self.ser = serial.Serial(device, baudrate)
    
    #         Y +100
    # X -100  center  X +100
    #         Y -100
    def move(self, x, y):
        linear = abs(int(y))
        steer = abs(int(x))
        if x >= 0:
            if y >= 0:
                command = 'rf'
            else:
                command = 'rb'
        else:
            if y >= 0:
                command = 'lf'
            else:
                command = 'lb'
        message = 'cmd:{},{},{}\n'.format(command, linear, steer)
        print(message)
        self.ser.write(message.encode('utf8'))
        
    def stop(self):
        self.ser.write(b'cmd:s,0,0\n')
    
    def close(self):
        self.ser.close()


device = 'COM5'
baudrate = 115200
ctrl = DriveController(device, baudrate)
ctrl.stop()

import time

for i in range(30, 100, 10):
    ctrl.move(i, i)
    time.sleep(2)
    ctrl.move(-i, i)
    time.sleep(2)
    ctrl.move(i, -i)
    time.sleep(2)
    ctrl.move(-i, -i)
    time.sleep(2)

ctrl.stop()
ctrl.stop()
ctrl.close()