import time
import board
import keypad

keyMatrix = keypad.KeyMatrix(
    row_pins = (board.D12, board.D11, board.D10, board.D9),
    column_pins = (board.D6, board.D5, board.SCL)
    )

while True: 
    event = keyMatrix.events.get()
    if event:
        print(event)
    time.sleep(0.01)

