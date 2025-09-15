from machine import Pin
from time import sleep

# LED ulkoisessa piirissä, GPIO18
led = Pin(18, Pin.OUT)

while True:
    led.toggle()
    sleep(0.5)   # puolen sekunnin välein
