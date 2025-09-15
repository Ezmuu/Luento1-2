from machine import Pin
from time import sleep_ms

# LED ulkoinen (GPIO18)
led = Pin(18, Pin.OUT)

# Button (GPIO13 <-> GND), sisäinen pull-up
btn = Pin(13, Pin.IN, Pin.PULL_UP)

while True:
    if btn.value() == 0:   # nappi pohjassa
        led.value(1)       # LED päälle
    else:
        led.value(0)       # LED pois
    sleep_ms(10)           # pieni viive