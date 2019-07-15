#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import RPi.GPIO as GPIO
import time
import atexit
import sys
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import define, options

atexit.register(GPIO.cleanup)
define("port", default=80, type=int)
####BOARD######
# F289N
IN1 = 11
IN2 = 12
IN3 = 13
IN4 = 15
# G90
OUT1 = 38
OUT2 = 40
i = 0
j = 0


####BOARD######

###steering###
def s_right():
    # print(233)
    global i
    print(i)
    if i - 10 >= 0:
        i = i - 10
        p.ChangeDutyCycle(2.5 + 10 * i / 180)
        time.sleep(0.02)
        p.ChangeDutyCycle(0)
        time.sleep(0.2)
    else:
        return 0


def s_left():
    global i
    if i + 10 < 181:
        i = i + 10
        p.ChangeDutyCycle(2.5 + 10 * i / 180)
        time.sleep(0.02)
        p.ChangeDutyCycle(0)
        time.sleep(0.2)
    else:
        return 0


def s_up():
    global j
    if j + 10 < 181:
        j = j + 10
        p2.ChangeDutyCycle(2.5 + 10 * j / 180)
        time.sleep(0.02)
        p2.ChangeDutyCycle(0)
        time.sleep(0.2)
    else:
        return 0


def s_down():
    global j
    if j - 10 >= 0:
        j = j - 10
        p2.ChangeDutyCycle(2.5 + 10 * j / 180)
        time.sleep(0.02)
        p2.ChangeDutyCycle(0)
        time.sleep(0.2)
    else:
        return 0


###car###
def init():
    GPIO.setmode(GPIO.BOARD)
    # F289N
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    # G90_PCM
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(OUT1, GPIO.OUT, initial=False)
    p = GPIO.PWM(OUT1, 50)
    p.start(0)
    GPIO.setup(OUT2, GPIO.OUT, initial=False)
    p2 = GPIO.PWM(OUT2, 50)
    p2.start(0)
    time.sleep(2)


#
def forward(tf):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(tf)
    GPIO.cleanup()


#
def reverse(tf):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(tf)
    GPIO.cleanup()


#
def left(tf):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(tf)
    GPIO.cleanup()


#
def right(tf):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(tf)
    GPIO.cleanup()


#
def pivot_left(tf):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(tf)
    GPIO.cleanup()


#
def pivot_right(tf):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(tf)
    GPIO.cleanup()


#
def p_left(tf):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(tf)
    GPIO.cleanup()


#
def p_right(tf):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(tf)
    GPIO.cleanup()


def data_dumps(data, arg):
    data["info"] = 1
    data["data"] = "成功，键入的按键为" + arg
    return json.dumps(data, encoding='gbk')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        init()
        flag = 1
        sleep_time = 0.1
        arg = self.get_argument('k')
        data = {
            'info': 0,
            'data': ''
        }
        if (arg == 'w'):
            forward(sleep_time)
        elif (arg == 's'):
            reverse(sleep_time)
        elif (arg == 'a'):
            left(sleep_time)
        elif (arg == 'd'):
            right(sleep_time)
        elif (arg == 'q'):
            pivot_left(sleep_time)
        elif (arg == 'e'):
            pivot_right(sleep_time)
        elif (arg == 'z'):
            p_left(sleep_time)
        elif (arg == 'x'):
            p_right(sleep_time)
        elif (arg == 'i'):
            if s_up() == 0:
                flag = 0
        elif (arg == 'k'):
            if s_down() == 0:
                flag = 0
        elif (arg == 'j'):
            if s_left() == 0:
                flag = 0
        elif (arg == 'l'):
            if s_right() == 0:
                flag = 0
        else:
            return False
        if flag == 1:
            self.write(data_dumps(data, str(arg)))
        else:
            self.write(json.dumps(data))


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

