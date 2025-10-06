# Luento1–2 — IoT-perusteet

Tämä repo sisältää:
- **Luento 1**: Wokwi + Raspberry Pi Pico W -harjoitukset (MicroPython)
- **Luento 2**: Weather Station – laitteen mittaukset → ThingSpeak, sekä pieni katselusivu (Google Charts)

---

## Sisältö
Luento1-2/
├─ Luento1/
│ ├─ <tehtävä1>/
│ │ ├─ main.py
│ │ └─ diagram.json
│ ├─ <tehtävä2>/
│ ├─ lcdtest/ # I2C-näyttötestit
│ ├─ weatherstation/ # DHT22 tms. + ThingSpeak-kirjoitus
│ └─ ... # muut Wokwi/Pico-harjoitukset
└─ Luento2/
├─ fetch_temperature.html # Google Charts -linechart
└─ fetch_temperature.js # hakee ThingSpeakistä (READ API KEY)


> **Huom.** Luento 3 (Express + SQLite) ja Luento 4 (Webhook/WebSocket) ovat erillisissä repoissa.

---

## Vaatimukset

- Wokwi-tili (selainsimulaattori Pico W:lle)
- Raspberry Pi Pico W (tai Wokwi-virtuaalilauta)
- (Luento 2 katseluun) Moderni selain; vaihtoehtoisesti kevyt http-palvelin (esim. `npx http-server` tai `python -m http.server`)

---

## Luento 1 – Wokwi + Pico W

Harjoituksia (esimerkkejä):
- Board-LED vilkkuminen / päälle-nappi
- Ulkoisen LEDin ohjaus + potentiometri (PWM-kirkkaus)
- Sisäinen lämpötila / ulkoinen anturi (esim. **DHT22**)
- Tapahtumat (button down/up) → lähetys **ThingSpeakiin**

### ThingSpeak-kirjoitus (MicroPython)
- Aseta **WRITE_API_KEY** ja lähetä esim. `field1` lämpötilalle:

```python
import network, time, urequests, dht
from machine import Pin

SSID = 'Wokwi-GUEST'
PASS = ''
WRITE_API_KEY = '<YOUR_THINGSPEAK_WRITE_KEY>'
URL = 'https://api.thingspeak.com/update'

sensor = dht.DHT22(Pin(15))

# WiFi-yhteys
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASS)
while not wlan.isconnected():
    time.sleep(0.2)

# Mittaus + lähetys
sensor.measure()
temp = sensor.temperature()
urequests.post(URL,
    data='api_key={}&field1={}'.format(WRITE_API_KEY, temp),
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
).close()



