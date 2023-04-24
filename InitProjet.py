# pyright: reportShadowedImports=false
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import time
import board
import neopixel
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
import pwmio
import adafruit_dht
from adafruit_motor import servo, motor
import mfrc522
from adafruit_tca8418 import TCA8418
import adafruit_hcsr04



#========================================== Déclaration variables etape 1 ==========================================
#Définit le lecteur de carte
RFID = mfrc522.MFRC522(board.D12, board.D11, board.D10, board.D9, board.D13)
RFID.set_antenna_gain(0x07 << 4)

#Définit le code de la carte
codeCarte = [61, 165, 79, 55, 224]

#========================================== Déclaration variables etape 2 ==========================================
# #Déclarer l'extantion
tca = TCA8418(board.I2C())

# turn on INT output pin
tca.key_intenable = True

#Déclare la switch sur l'extantion
switch = TCA8418.C8
tca.gpio_mode[switch] = True


# set up all R0-R2 pins and C0-C3 pins as keypads
matrixPins = (
    TCA8418.R0,
    TCA8418.R1,
    TCA8418.R2,
    TCA8418.C0,
    TCA8418.C1,
    TCA8418.C2,
    TCA8418.C3,
)

# make them inputs with pullups
for pin in matrixPins:
    tca.keypad_mode[pin] = True
    # make sure the key pins generate FIFO events
    tca.enable_int[pin] = True
    # we will stick events into the FIFO queue
    tca.event_mode_fifo[pin] = True

#Déclarer la carte des touches du clavier matrix
keymap = (("*", "0", "#"), ("7", "8", "9"), ("4", "5", "6"), ("1", "2", "3"))

aeroports =  {
                "101" : "YUL Montreal", 
                "111" : "ATL Atlanta",
                "222" : "HND Tokyo",
                "764" : "LHR London", 
                "492" : "CAN Baiyun",
                "174" : "CDG Paris",
                "523" : "AMS Amsterdam",  
            }
#========================================== Déclaration variables etape 3 ==========================================
# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D6)

#déclarer servomoteurs
ServoPwm = pwmio.PWMOut(board.D5, duty_cycle=2 ** 15, frequency=50)
servoMoteur = servo.Servo(ServoPwm, min_pulse=500, max_pulse= 2500)
servoMoteur.angle = 90

#déclarer moteur DC
pwmDCMotor1 = pwmio.PWMOut(board.A0)
pwmDCMotor2 = pwmio.PWMOut(board.A1)
DCMotor = motor.DCMotor(pwmDCMotor1, pwmDCMotor2)
DCMotor.throttle = 0

#déclarer joystick
joystickX = AnalogIn(board.A2)
joystickY = AnalogIn(board.A3)
joystickSW = DigitalInOut(board.A4)
joystickSW.direction = Direction.INPUT   
joystickSW.pull = Pull.UP

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.RX, echo_pin=board.TX)

#déclarer l'anneau neopixel
anneauNeo = neopixel.NeoPixel(board.A5, 8, brightness=0.5, auto_write=False)

#========================================== Déclaration variables Global ==========================================
neoLed = neopixel.NeoPixel(board.NEOPIXEL, 1)
neoLed.brightness = 0.05
neoLed[0] = (255,255,255)

# Déclarer les dictionnaires 
couleurNeo = {
                "rouge" : (255, 0, 0),
                "jaune" : (255, 200, 0),
                "vert"  : (0, 255, 0),
                "blanc" : (255, 255, 255),
                "noir" : (0,0,0)
            }
    
#Déclarer la variable global "destination" 
destination = ""

#========================================== Gestion du wifi ==========================================

timerWifi = time.monotonic()

key = "O1MV7NRO1B07USO7"
URL = "https://api.thingspeak.com/update.json"

socket = socketpool.SocketPool(wifi.radio)
context = ssl.create_default_context()
https = adafruit_requests.Session(socket, context)

        
def envoisWifi():
    global timerWifi
    if timerWifi + 5 <= time.monotonic():
        json_data = {
            "api_key" : key,
            "field1": dhtDevice.temperature,
            "field2" : dhtDevice.humidity
        }
        response = https.post(URL, json = json_data)
        timerWifi = time.monotonic()