# Luento1–2 — IoT-perusteet

Tämä repo sisältää:
- **Luento 1:** Wokwi + Raspberry Pi Pico W -harjoitukset (MicroPython)
- **Luento 2:** Weather Station – mittaukset ThingSpeakiin 

> Huom: **Luento 3** (Express + SQLite) ja **Luento 4** (Webhook / WebSocket) ovat erillisissä repoissa.

---

## Sisällysluettelo
- [Projektirakenne](#projektirakenne)
- [Vaatimukset](#vaatimukset)
- [Luento 1 – Wokwi + Pico W](#luento-1--wokwi--pico-w)
  - [ThingSpeakiin lähetys (MicroPython-esimerkki)](#thingspeakiin-lähetys-micropython-esimerkki)
- [Luento 2 – Weather Station (katselu)](#luento-2--weather-station-katselu)
  - [Google Charts -LineChart (esimerkkikoodi)](#google-charts--linechart-esimerkkikoodi)
  - [Käynnistys ja käyttö](#käynnistys-ja-käyttö)
- [Vianetsintä](#vianetsintä)
- [.gitignore-suositus](#gitignore-suositus)
- [Lisenssi](#lisenssi)

---


## Vaatimukset

- **Wokwi**-tili (Pico W -simulaatiot)
- **Raspberry Pi Pico W** (tai Wokwi-virtuaalilauta)
- (Luento 2 katseluun) Moderni selain; tarvittaessa kevyt http-palvelin:
  - `npx http-server` **tai**
  - `python -m http.server` (Python 3)

---

## Luento 1 – Wokwi + Pico W

Harjoituksia (esimerkkejä):
- Board-LED vilkkuminen / päälle-nappi
- Ulkoisen LEDin ohjaus + potentiometri (PWM-kirkkaus)
- Sisäinen lämpötila / ulkoinen anturi (esim. **DHT22**)
- Button down → LED on + lähetä **ThingSpeakiin** (button up → off)

Tyypilliset tiedostot: `main.py`, `diagram.json` (Wokwi-kaavio, sensorien pinnit yms.).

### ThingSpeakiin lähetys (MicroPython-esimerkki)


```python
# main.py (esimerkki: DHT22 lämpötila -> ThingSpeak field1)
import network, time, urequests, dht
from machine import Pin

SSID = 'Wokwi-GUEST'
PASS = ''
WRITE_API_KEY = '<YOUR_THINGSPEAK_WRITE_KEY>'
URL = 'https://api.thingspeak.com/update'

sensor = dht.DHT22(Pin(15))   # säädä GP-pin Wokwi-kaavion mukaan

# WiFi-yhteys
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASS)
while not wlan.isconnected():
    time.sleep(0.2)

# Mittaus + lähetys (kertaluonteinen esimerkki)
sensor.measure()
temp = sensor.temperature()
try:
    resp = urequests.post(
        URL,
        data='api_key={}&field1={}'.format(WRITE_API_KEY, temp),
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    resp.close()
except Exception as e:
    print("HTTP error:", e)
