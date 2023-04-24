import board
import time
import pwmio
from adafruit_motor import servo
# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.A3, duty_cycle=2 ** 15, frequency=50)

#déclarer Moteurs
servoMoteur = servo.Servo(pwm, min_pulse=500, max_pulse= 2500)
servoMoteur.angle = 0

#Tests de materiel
def testServomoteur():
    for angle in range(0, 180, 1):  # 0 - 180 degrees, 5 degrees at a time.
        servoMoteur.angle = angle
        time.sleep(0.03)
    for angle in range(180, 0, -1): # 180 - 0 degrees, 5 degrees at a time.
        servoMoteur.angle = angle
        time.sleep(0.03)
    
while True:
    testServomoteur()
    time.sleep(0.1)
