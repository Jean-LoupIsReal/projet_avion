"""
Example of reading from a card using the ``mfrc522`` module.
"""
# pyright: reportShadowedImports=false

# 3rd party
import board

# this package
import mfrc522
import time

key = [61, 165, 79, 55, 224]

def do_read():

	RFID = mfrc522.MFRC522(board.D12, board.D11, board.D10, board.D9, board.D6)
	RFID.set_antenna_gain(0x07 << 4)

	print('')
	print("Place card before reader to read from address 0x08")
	print('')
	try:
		while True:
			(stat, tag_type) = RFID.request(RFID.REQIDL)

			if stat == RFID.OK:

				(stat, raw_uid) = RFID.anticoll()
                
				if stat == RFID.OK:
					print("New card detected")
					print("  - tag type: 0x%02x" % tag_type)
					print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print(raw_uid)

	except KeyboardInterrupt:
		print("Bye")