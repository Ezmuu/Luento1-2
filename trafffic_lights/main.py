from machine import Pin
from time import sleep

# LEDit ja summeri
red = Pin(15, Pin.OUT)
yellow = Pin(14, Pin.OUT)
green = Pin(13, Pin.OUT)
buzzer = Pin(12, Pin.OUT)

# Button (GP16 <-> 3V3, sisäinen pull-down)
btn = Pin(16, Pin.IN, Pin.PULL_DOWN)

def all_off():
    red.value(0)
    yellow.value(0)
    green.value(0)
    buzzer.value(0)

while True:
    if btn.value() == 1:   # nappi painettu -> HIGH
        all_off()
        red.value(1)
        buzzer.value(1)
        sleep(2)           # summeri soi 2 s
        buzzer.value(0)
        sleep(2)           # punainen vielä päällä
    else:
        # normaali liikennevalokierto
        all_off()
        green.value(1)
        sleep(3)
        
        all_off()
        yellow.value(1)
        sleep(1)
        
        all_off()
        red.value(1)
        sleep(3)
