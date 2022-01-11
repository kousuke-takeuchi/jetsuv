from rusb import USB
from _thread import start_new_thread
from machine import PWM, Pin
from time import sleep_ms

# USB初期化
usb = USB()

input_msg = None
bufferSTDINthread = start_new_thread(usb.bufferSTDIN, ())


# モーター初期化
IN1 = PWM(Pin(1))
IN2 = PWM(Pin(2))
IN1.freq(100)
IN2.freq(100)

max_duty = 65025

while True:
    # USBシリアルからコマンド列を受信
    input_msg = usb.getLineBuffer()

    # PWMでモーターの制御サンプル
    # 正転
    IN2.duty_u16(0)
    for i in range(50, 100):
        IN1.duty_u16(int(max_duty+*i*0.01))
        sleep_ms(100)

    # ブレーキ
    IN1.duty_u16(max_duty)
    IN2.duty_u16(max_duty)
    sleep_ms(2000)
    
    # 逆回転
    IN1.duty_u16(0)
    for i in range(50, 100):
        IN2.duty_u16(int(max_duty+*i*0.01))
        sleep_ms(100)
    
    # 停止
    IN1.duty_u16(0)
    IN2.duty_u16(0)
    sleep_ms(2000)
    
    sleep_ms(10)