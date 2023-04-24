import board
import time
import neopixel
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from rainbowio import colorwheel


#déclarer potentiometre
potentiometre = AnalogIn(board.A1)

pixels = neopixel.NeoPixel(board.A2, 8, brightness=0.05, auto_write=False)

WHITE = (255, 255, 255)
BLACK = (0,0,0)
while True:
    nbLed = int(((potentiometre.value-417) * 8)/(52964-417))
    for i in range(nbLed):
        pixels[i] = WHITE
    for i in range(nbLed, 8):
        pixels[i] = BLACK
    pixels.show()
    time.sleep(0.1)
