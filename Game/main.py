from machine import Pin
import utime, urandom

# --- pinnit ---
led = Pin(15, Pin.OUT, value=0)          # ulkoinen LED
btn = Pin(14, Pin.IN, Pin.PULL_DOWN)     # nappi GP14 <-> 3V3

# --- tilamuuttujat ---
timer_start = 0
pressed_time = 0
waiting_for_press = False
pressed_flag = False

def on_press(pin):
    global pressed_time, pressed_flag, waiting_for_press
    if waiting_for_press:
        pressed_time = utime.ticks_ms()
        pressed_flag = True
        btn.irq(handler=None)   # one-shot

def random_delay_ms(lo=1500, hi=4000):
    span = hi - lo + 1
    return lo + (urandom.getrandbits(16) % span)

while True:
    # odota että nappi ei ole pohjassa
    while btn.value():
        utime.sleep_ms(5)

    # LED päälle = valmius
    led.value(1)
    utime.sleep_ms(random_delay_ms())

    # LED pois = GO
    led.value(0)
    timer_start = utime.ticks_ms()
    waiting_for_press = True
    pressed_flag = False
    btn.irq(trigger=Pin.IRQ_RISING, handler=on_press)

    # odota painallus
    while not pressed_flag:
        utime.sleep_ms(1)

    # reaktioaika
    reaction_ms = utime.ticks_diff(pressed_time, timer_start)
    print("Reaction time:", reaction_ms, "ms")

    # pieni tauko ennen seuraavaa kierrosta
    waiting_for_press = False
    utime.sleep_ms(1000)
