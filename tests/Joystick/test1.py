import math
import time
import board
from analogio import AnalogIn

#déclarer joystick
joystickX = AnalogIn(board.A2)
joystickY = AnalogIn(board.A3)

def valeurJoystick(joystickValeur):
    #transforme valeur potentiometre en valeur entre -1 et 1
    if joystickValeur < 29000:
        valeur = ((30000-joystickValeur-500)/25000)*1
    elif joystickValeur > 38000:
        valeur = ((joystickValeur - 38000)/(52000-38000))*-1
    else:
        valeur = 0
    
    #s'assure que les valeurs soient bien entre -1 et 1
    if valeur < -1:
        valeur = -1
    elif valeur > 1:
        valeur = 1
    
    return valeur

#Calcul l'angle du joystick selon arctan2 (cercle trigonometrique)
def angleJoystick(x, y):
    angle = math.degrees(math.atan2(y, x))
    return angle % 360

while True:
    valX = valeurJoystick(joystickX.value)
    valY = valeurJoystick(joystickY.value)
    print(angleJoystick(valX, valY))