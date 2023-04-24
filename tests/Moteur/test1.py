"""Correction"""
import time
import board
import pwmio
from adafruit_motor import motor
pwmDCMotor1 = pwmio.PWMOut(board.D5)
pwmDCMotor2 = pwmio.PWMOut(board.D6)
DCMotor = motor.DCMotor(pwmDCMotor1, pwmDCMotor2)
DCMotor.throttle = 0


# ===Tests pour les composants===
# test Moteur
x = 0.01

while True:

    if DCMotor.throttle >0.99:
       x = x * -1 
       print(DCMotor.throttle)
       DCMotor.throttle += x
    elif DCMotor.throttle < -0.99:
        x = x * -1
        DCMotor.throttle += x
    
    DCMotor.throttle += x

    print(DCMotor.throttle)
    time.sleep(0.05)