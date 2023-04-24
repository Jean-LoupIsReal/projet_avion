import board
import neopixel
import time
import pwmio
import adafruit_hcsr04
from adafruit_motor import servo
import board
import adafruit_dht

#déclare dht
dht = adafruit_dht.DHT11(board.D6)

while True:
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        # Print what we got to the REPL
        print("Temp: {:.1f} *C \t Humidity: {}%".format(temperature, humidity))
    except RuntimeError as e:
        # Reading doesn't always work! Just print error and we'll try again
        print("Reading from DHT failure: ", e.args)
    time.sleep(1)