from machine import Pin, PWM
import random
import time
        
takki1 = Pin(10, Pin.IN, Pin.PULL_UP)
takki2 = Pin(11, Pin.IN, Pin.PULL_UP)
takki3 = Pin(12, Pin.IN, Pin.PULL_UP)
takki4 = Pin(13, Pin.IN, Pin.PULL_UP)
takki5 = Pin(14, Pin.IN, Pin.PULL_UP)


led_red1 = Pin(10, Pin.OUT)
led_red2 = Pin(14, Pin.OUT)

led_green1 = Pin(11, Pin.OUT)
led_green2 = Pin(12, Pin.OUT)
led_green3 = Pin(13, Pin.OUT)


def takka_ytta():
    if takki1.value() = 0:
        print("rauða takki 1 var ýtt á")
        led_red1.value(1)
        
    elif takki2.value() = 0:
        print("grænni takki 1 var ýtt á")
        led_green1.value(1)
    
    elif takki3.value() = 0:
        print("grænni takki 2 var ýtt á")
        led_green2.value(1)
    
    elif takki4.value() = 0:
        print("grænni takki 3 var ýtt á")
        led_green3.value(1)
    
    elif takki1.value() = 0:
        print("rauða takki 1 var ýtt á")
        led_red2.value(1)

takka_ytta()
        
        