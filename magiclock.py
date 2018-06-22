#!/usr/bin/env python3

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import sleep

sense = SenseHat() # init senseHat

# tuples: (Roll,pitch,yaw) or (DirectionJoyStick)

"""
up: 1
down: 2
left: 3
right: 4
"""
sequence = [(1.0,0.0,0.0),(0.0,1.0,0.0),(1.0,0.0,0.0),(1.0,0.0,0.0)]

R = [255, 0, 0]  # Red
G = [127, 255, 0] # Green
O = [255, 255, 255]  # White

display =	[O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O,
 			O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O]

j=0
for k in sequence: # remplir le display d'aussi bcp de nombres que d'element dans la sequence
	display[j] = R
	j=j+1

sense.set_pixels(display)
sense.low_light = True

threshold = 0.12 # pour le bruit/imperfections

def close(x,value,threshold):
	if (x > (value-threshold) and x < (value+threshold)):	
		return True
	else:
		return False

sense.set_imu_config(False, False, True) # active seulement l'accelerometre

notUnlocked = True
i = 0 # position dans la sequence
print("Pivoter puis valider la position")
while notUnlocked:
	event = sense.stick.wait_for_event()
	if event.action != ACTION_RELEASED: # seulement quand on appuye sur le joystick
		acc = sense.get_accelerometer_raw()
		x = acc['x']
		y = acc['y']
		z = acc['z']
		if (close(x,sequence[i][0],threshold) and close(y,sequence[i][1],threshold) and close(z,sequence[i][2],threshold)): # toutes les directions doivent etre bonnes
			display[i] = G
			sense.set_pixels(display)
			i = i+1
			print("bravo! (%s/%s)"%(str(i),str(len(sequence))))
		else:
			i = 0
			j = 0
			for k in sequence: # remettre le display 
				display[j] = R
				j=j+1
			sense.set_pixels(display)
			print("on recommence...")
	if (i >= len(sequence)):
		notUnlocked = False # pour sortir de la boucle quand la sequence à bien été reproduite

sense.show_message("Secret message", text_colour=[255, 0, 0]) # Message secret s'affiche sur le panel LED


