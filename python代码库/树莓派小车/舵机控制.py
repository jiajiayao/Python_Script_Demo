#-*- coding: utf-8 -*-


import RPi.GPIO as GPIO
import time
import signal
import atexit

GPIO.setwarnings(False)
atexit.register(GPIO.cleanup)
servopin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT, initial=False)
p = GPIO.PWM(servopin, 50)  # 50HZ
p.start(0)
time.sleep(2)

i=0
while (True):
    str=raw_input()
    if str=='q':

        i=i+10
        if i>181:
            i=i-10
        p.ChangeDutyCycle(2.5 + 10 * i / 180)  # 设置转动角度
        time.sleep(0.02)  # 等该20ms周期结束


    if str=='w':
        i=i-10
        if i<0:
            i=i+10
        p.ChangeDutyCycle(2.5 + 10 * i / 180)
        time.sleep(0.02)

