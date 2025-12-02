from machine import Pin
import time

takki1_raud = Pin(9, Pin.IN, Pin.PULL_UP)
takki2_raud = Pin(14,  Pin.IN, Pin.PULL_UP)
                  
takki1_graen = Pin(11, Pin.IN, Pin.PULL_UP)
takki2_graen = Pin(12, Pin.IN, Pin.PULL_UP)
takki3_graen = Pin(13,  Pin.IN, Pin.PULL_UP)


led_red1   = Pin(16, Pin.OUT)
led_red2   = Pin(3, Pin.OUT)
led_green1 = Pin(17, Pin.OUT)
led_mid = Pin(18, Pin.OUT)
led_green2 = Pin(8, Pin.OUT)

leds = [led_red1, led_green1, led_mid, led_green2, led_red2]

def slokkva_allt():
    for d in leds:
        d.value(0)

slokkva_allt()
while True:

#rauða takki 1
    if takki1_raud.value() == 0:
        print("rauða takki 1 var ýtt á")
        led_red1.value(1)
        time.sleep_ms(500)
        slokkva_allt()
#Grænni takki 1
    elif takki1_graen.value() == 0:
        print("grænni takki 1 var ýtt á")
        led_green1.value(1)
        time.sleep_ms(500)
        slokkva_allt()
#Mið takki 2
    elif takki2_graen.value() == 0:
        print("grænni takki 2 var ýtt á")
        led_mid.value(1)
        time.sleep_ms(500)
        slokkva_allt()
#Grænni takki 3
    elif takki3_graen.value() == 0:
        print("grænni takki 3 var ýtt á")
        led_green2.value(1)
        time.sleep_ms(500)
        slokkva_allt()
#rauða takki 2
    elif takki2_raud.value() == 0:
        print("rauða takki 2 var ýtt á")
        led_red2.value(1)
        time.sleep_ms(500)
        slokkva_allt()

    time.sleep_ms(10)  # smá "debounce" og til að létta á CPU