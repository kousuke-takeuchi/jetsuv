from sys import stdin, exit
from machine import PWM, Pin
from time import sleep_ms
from _thread import start_new_thread

# モーター初期化
FRONT_IN1 = PWM(Pin(1))
FRONT_IN2 = PWM(Pin(6))
BACK_IN1 = PWM(Pin(2))
BACK_IN2 = PWM(Pin(3))
STEER_IN1 = PWM(Pin(4))
STEER_IN2 = PWM(Pin(5))

FRONT_IN1.freq(100)
FRONT_IN2.freq(100)
BACK_IN1.freq(100)
BACK_IN2.freq(100)
STEER_IN1.freq(100)
STEER_IN2.freq(100)

MAX_DUTY = 65025


# 正転
def left_front(linear_rate=1.0, steer_rate=1.0):
    FRONT_IN2.duty_u16(0)
    FRONT_IN1.duty_u16(int(MAX_DUTY * linear_rate))
    BACK_IN2.duty_u16(0)
    BACK_IN1.duty_u16(int(MAX_DUTY * linear_rate))
    STEER_IN2.duty_u16(0)
    STEER_IN1.duty_u16(int(MAX_DUTY * steer_rate))


def right_front(linear_rate=1.0, steer_rate=1.0):
    FRONT_IN2.duty_u16(0)
    FRONT_IN1.duty_u16(int(MAX_DUTY * linear_rate))
    BACK_IN2.duty_u16(0)
    BACK_IN1.duty_u16(int(MAX_DUTY * linear_rate))
    STEER_IN1.duty_u16(0)
    STEER_IN2.duty_u16(int(MAX_DUTY * steer_rate))


# 逆回転
def left_back(linear_rate=1.0, steer_rate=1.0):
    FRONT_IN1.duty_u16(0)
    FRONT_IN2.duty_u16(int(MAX_DUTY * linear_rate))
    BACK_IN1.duty_u16(0)
    BACK_IN2.duty_u16(int(MAX_DUTY * linear_rate))
    STEER_IN2.duty_u16(0)
    STEER_IN1.duty_u16(int(MAX_DUTY * steer_rate))


def right_back(linear_rate=1.0, steer_rate=1.0):
    FRONT_IN1.duty_u16(0)
    FRONT_IN2.duty_u16(int(MAX_DUTY * linear_rate))
    BACK_IN1.duty_u16(0)
    BACK_IN2.duty_u16(int(MAX_DUTY * linear_rate))
    STEER_IN1.duty_u16(0)
    STEER_IN2.duty_u16(int(MAX_DUTY * steer_rate))


# ブレーキ
def stop():
    FRONT_IN1.duty_u16(0)
    FRONT_IN2.duty_u16(0)
    BACK_IN1.duty_u16(0)
    BACK_IN2.duty_u16(0)
    STEER_IN1.duty_u16(0)
    STEER_IN2.duty_u16(0)


class USB:
    buffer_size = 1024
    buffer = [' '] * buffer_size
    buffer_echo = True
    buffer_next_in, buffer_next_out = 0, 0
    terminated_thread = False
    
    def buffer_stdin(self):
        while True:
            if self.terminated_thread:
                break
            self.buffer[self.buffer_next_in] = stdin.read(1)
            if self.buffer_echo:
                print(self.buffer[self.buffer_next_in], end='')
            self.buffer_next_in += 1
            if self.buffer_next_in == self.buffer_size:
                self.buffer_next_in = 0

    def get_byte_buffer(self):
        if self.buffer_next_out == buffer_next_in:
            return ''
        n = self.buffer_next_out
        self.buffer_next_out += 1
        if self.buffer_next_out == self.buffer_size:
            self.buffer_next_out = 0
        return (self.buffer[n])

    def get_line_buffer(self):
        if self.buffer_next_out == self.buffer_next_in:
            return ''

        n = self.buffer_next_out
        while n != self.buffer_next_in:
            if self.buffer[n] == '\x0a': 
                break
            n += 1
            if n == self.buffer_size:
                n = 0
        if (n == self.buffer_next_in):
            return ''

        line = ''
        n += 1
        if n == self.buffer_size:
            n = 0

        while self.buffer_next_out != n:
            
            if self.buffer[self.buffer_next_out] == '\x0d':
                self.buffer_next_out += 1
                if self.buffer_next_out == self.buffer_size:
                    self.buffer_next_out = 0
                continue
            
            if self.buffer[self.buffer_next_out] == '\x0a':
                self.buffer_next_out += 1
                if self.buffer_next_out == self.buffer_size:
                    self.buffer_next_out = 0
                break
            line = line + self.buffer[self.buffer_next_out]
            self.buffer_next_out += 1
            if self.buffer_next_out == self.buffer_size:
                self.buffer_next_out = 0
        return line                    


def main():
    usb = USB()
    start_new_thread(usb.buffer_stdin, ())
    
    stop()
    
    while True:
        input_msg = usb.get_line_buffer()
        if input_msg and 'cmd' in input_msg:
            data = input_msg.strip().replace('cmd:', '')
            command, linear_rate, steer_rate = data.split(',')
            linear_rate = int(linear_rate) / 100
            steer_rate = int(steer_rate) / 100
            if command == 'lf':
                left_front(linear_rate, steer_rate)
            if command == 'lb':
                left_back(linear_rate, steer_rate)
            if command == 'rf':
                right_front(linear_rate, steer_rate)
            if command == 'rb':
                right_back(linear_rate, steer_rate)
            if command == 's':
                stop()
        sleep_ms(10)

main()