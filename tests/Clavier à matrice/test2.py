import time
import board
import keypad
#import neopixel

keyMatrix = keypad.KeyMatrix(
    row_pins = (board.D12, board.D11, board.D10, board.D9),
    column_pins = (board.D6, board.D5, board.SCL)
    )

chiffreFinal = 0
chiffreEntre = ""
tableValKeypad = {
                    0:"1", 
                    1:"2", 
                    2:"3", 
                    3:"4", 
                    4: "5",
                    5: "6",
                    6: "7",
                    7: "8",
                    8: "9",
                    10: "0",
                }
x = 0
while True:
    event = keyMatrix.events.get()
    if event:
        #event.pressed ne voulait pas marcher
        if x == 0:
            if event.key_number == 9:
                chiffreFinal = int(chiffreEntre) * int(chiffreEntre)
                print("La valeur final est :", chiffreFinal)
                chiffreEntre = ""
            else:
                try:
                    chiffreEntre += tableValKeypad[event.key_number]
                    print(chiffreEntre)
                except:
                    print("le # n'est pas une entrée valide")
            x += 1
        else:
            x = 0
    time.sleep(0.1)

