from sense_hat import SenseHat, ACTION_PRESSED, ACTION_RELEASED, ACTION_HELD
import os
from time import gmtime, strftime

sense = SenseHat()


DURATION = 10 # in seconds!

# Color code
R = [255, 0, 0]
G = [127, 255, 0]
O = [255, 255, 255]

# Some image to display
green = [R] * 64
red = [G] * 64

sense.set_pixels(green)

print("Appuyer sur le joystick pour enregistrer")
event = sense.stick.wait_for_event()
while event.action != ACTION_RELEASED:
    event = sense.stick.wait_for_event()

sense.set_pixels(red)

TIMESTAMP = strftime("%Y-%m-%d-%H:%M", gmtime())

# record sensehat for DURATION seconds and store in 'data_TIMESTAMP.hat'
os.system("sense_rec -d %s data_%s.hat"%(DURATION,TIMESTAMP))
print("Data logged in: data_%s"%(TIMESTAMP))

sense.clear()




