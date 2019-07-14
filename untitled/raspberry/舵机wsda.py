import RPi.GPIO as GPIO
import time
import signal
import atexit

import os
import sys
import tty, termios

atexit.register(GPIO.cleanup)

servopin = 22
servopin2 = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT, initial=False)
p = GPIO.PWM(servopin, 50)
p.start(0)

GPIO.setup(servopin2, GPIO.OUT, initial=False)
p2 = GPIO.PWM(servopin2, 50)
p2.start(0)
time.sleep(2)

i = 0
j = 0
while True:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == 'a':
        if i - 10 >= 0:
            i = i - 10
            p.ChangeDutyCycle(2.5 + 10 * i / 180)
            time.sleep(0.02)
            p.ChangeDutyCycle(0)
            time.sleep(0.2)
    if ch == 'd':
        if i + 10 < 181:
            i = i + 10
            p.ChangeDutyCycle(2.5 + 10 * i / 180)
            time.sleep(0.02)
            p.ChangeDutyCycle(0)
            time.sleep(0.2)
    if ch == 'w':
        if j + 10 < 181:
            j = j + 10
            p2.ChangeDutyCycle(2.5 + 10 * j / 180)
            time.sleep(0.02)
            p2.ChangeDutyCycle(0)
            time.sleep(0.2)
    if ch == 's':
        if j - 10 >= 0:
            j = j - 10
            p2.ChangeDutyCycle(2.5 + 10 * j / 180)
            time.sleep(0.02)
            p2.ChangeDutyCycle(0)
            time.sleep(0.2)
    if ch == 'q':
        print
        "shutdown"
        break;
