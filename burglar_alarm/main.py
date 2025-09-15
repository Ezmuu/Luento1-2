from machine import Pin
import utime

PIR_PIN = 16                 # pir1:OUT -> GP16
LED = Pin("LED", Pin.OUT)    # sisäinen LED (GPIO25)
pir = Pin(PIR_PIN, Pin.IN)   # PIR antaa valmiiksi TTL-tason 0/1

# yksinkertainen "cooldown", ettei tule tulvasta monta ilmoitusta
last_ms = 0
COOLDOWN_MS = 2000

def on_motion(pin):
    global last_ms
    now = utime.ticks_ms()
    if utime.ticks_diff(now, last_ms) < COOLDOWN_MS:
        return
    last_ms = now

    # Ilmoitus käyttäjälle
    print("Motion detected!")
    LED.value(1)
    utime.sleep_ms(300)
    LED.value(0)

# PIRin OUT menee HIGH liikkeestä -> kuunnellaan nousevaa reunaa
pir.irq(trigger=Pin.IRQ_RISING, handler=on_motion)

print("Burglary alarm armed.")
while True:
    utime.sleep_ms(100)   # pidä ohjelma hengissä
