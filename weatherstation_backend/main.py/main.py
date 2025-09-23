import network           # For Wi-Fi connectivity
import time              # For delays and timing
import urequests         # For making HTTP requests
import dht               # For interfacing with DHT sensors
from machine import Pin  # For controlling GPIO pins

ssid = 'Wokwi-GUEST'     # SSID of the Wi-Fi network
password = ''            # Password (empty for open networks like Wokwi-GUEST)

THINGSPEAK_API_KEY = 'RM7YP4Y0C4JZEF71'                  # Your ThingSpeak Write API Key
THINGSPEAK_URL = 'https://api.thingspeak.com/update'     # ThingSpeak endpoint

wlan = network.WLAN(network.STA_IF)     # Create a WLAN object in station mode,
                                        # the device connects to a Wi-Fi network as a client.
                                        # Other option: AP_IF, Access Point mode –
                                        # the device creates its own Wi-Fi network (hotspot).
wlan.active(True)                        # Activate the Wi-Fi interface
wlan.connect(ssid, password)             # Connect to the specified Wi-Fi network

print("Connecting to Wi-Fi...", end="")
while not wlan.isconnected():
    print(".", end="")                   # Print dots while waiting
    time.sleep(0.5)                      # Wait half a second before retrying

print("\nConnected!")
print("IP address:", wlan.ifconfig()[0])

sensor = dht.DHT22(Pin(15))

def send_to_thingspeak(temp):
    if temp is None:
        print("No temperature data to send.")
        return
    try:
        # Send HTTP POST request to ThingSpeak with temperature data
        response = urequests.post(
            THINGSPEAK_URL,
            data='api_key={}&field1={}'.format(THINGSPEAK_API_KEY, temp),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        print("ThingSpeak response:", response.text)  # Print server response
        response.close()  # Close the connection
    except Exception as e:
        print("Failed to send data:", e)  # Handle any errors


  
while True:
    try:
        sensor.measure()                              # Trigger sensor measurement
        temperature = sensor.temperature()            # Read temperature in Celsius
        print("Temperature:", temperature, "°C")      # Display temperature
        send_to_thingspeak(temperature)               # Send data to ThingSpeak
    except Exception as e:
        print("Error reading sensor or sending data:", e)  # Handle errors

    time.sleep(15)  # Wait 15 seconds before next reading
