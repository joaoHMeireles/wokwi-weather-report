import time
import network
from machine import Pin
import dht
import urequests
import json

# --------- // setup //----------

print("Connecting to WiFi", end="")

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')

while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)

print("Connected!")

sensor = dht.DHT22(Pin(15))

URL = "https://wokwi-weather-report.onrender.com/tago-io/weather/data"
headers = {}
headers['Content-Type'] = "application/json"

# --------- // actual program //----------

def create_weather_report(temperature, humidity):
  return {"temperature": temperature, "humidity": humidity}

prev_report = create_weather_report(None, None)

def changed_value(report):
  if prev_report["temperature"] == None or prev_report["humidity"] == None:
    return True

  changed_temperature = prev_report["temperature"] != report["temperature"]
  changed_humidity = prev_report["humidity"] != report["humidity"]

  return changed_temperature or changed_humidity

while True:
  print("Measuring weather conditions... ", end="")
  sensor.measure() 
  report = create_weather_report(sensor.temperature(), sensor.humidity())
  
  if changed_value(report):
    print("Updated!")
    print(report)

    try:
      data = json.dumps(report)

      response = urequests.post(url=URL, data=data, headers=headers).json()
      print(response)

      prev_report = report

    except Exception as exc:
      print(exc)

  else:
    print("No change")

  time.sleep(1)
