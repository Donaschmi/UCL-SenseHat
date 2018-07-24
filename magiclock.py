#!/usr/bin/env python3

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import sleep

sense = SenseHat() # init senseHat
sense.set_imu_config(False, False, True) # active seulement l'accelerometre
threshold = 0.2 # pour le bruit/imperfections

# tuples: (Roll,pitch,yaw) or (DirectionJoyStick) ! in Gs

"""
up: 1
down: 2
left: 3
right: 4
"""
sequence = [(1.0,0.0,0.0),(0.0,1.0,0.0),(1,)]

R = [255, 0, 0]  # Red
G = [127, 255, 0] # Green
O = [255, 255, 255]  # White

# Image blanche
display =	[O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O,
 			O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O]
# Image cadenas verrouiller
locked =	[O,O,O,O,O,O,O,O,
			O,O,R,R,R,R,O,O,
			O,O,R,O,O,R,O,O,
 			O,O,R,O,O,R,O,O,
			O,R,R,R,R,R,R,O,
			O,R,R,R,R,R,R,O,
			O,R,R,R,R,R,R,O,
			O,R,R,R,R,R,R,O]
# Image cadenas déverrouiller
unlocked =	[O,O,G,G,G,G,O,O,
			O,O,G,O,O,G,O,O,
			O,O,G,O,O,G,O,O,
 			O,O,O,O,O,G,O,O,
			O,G,G,G,G,G,G,O,
			O,G,G,G,G,G,G,O,
			O,G,G,G,G,G,G,O,
			O,G,G,G,G,G,G,O]
"""
	Pour déverrouiller, appuyer sur le joystick
"""
sense.set_pixels(locked)
event = sense.stick.wait_for_event()
while event.action != ACTION_RELEASED:
	event = sense.stick.wait_for_event()


"""
	affiche le nombre de position correcte à fournir
"""
j=0
for k in sequence:
	display[j] = R
	j=j+1
sense.set_pixels(display)
sense.low_light = True


"""
	renvoie vrai si x€[value-threshold,value+treshold] sinon faux
"""
def close(x,value,threshold):
	if (x > (value-threshold) and x < (value+threshold)):	
		return True
	else:
		return False
"""
	Renvoie la direction correspondante au number
"""
def translate(number):
	if (number == 1):
		return "up"
	elif (number == 2):
		return "down"
	elif (number == 3):
		return "left"
	elif (number == 4):
		return "right"
	else:
		return "up"

def reset_display(seq):
	j = 0
	for k in seq: # remettre le display 
		display[j] = R
		j=j+1
	sense.set_pixels(display)
	print("on recommence...")
	return 0

def advance(i):
	display[i] = G
	sense.set_pixels(display)
	p = i+1
	print("bravo! (%s/%s)"%(str(p),str(len(sequence))))
	return p


"""
	Corps central du script
"""
unlocked_bool = False
i = 0 # position dans la sequence
print("Faites vos combinaisons")
while not unlocked_bool:
	event = sense.stick.wait_for_event()
	if event.action != ACTION_RELEASED: # seulement quand on appuye sur le joystick
		if event.direction != "middle":
			if (len(sequence[i]) == 1 and translate(sequence[i]) == event.direction):
				i = advance(i)
			else:
				i = reset_display(sequence)
		else:
			acc = sense.get_accelerometer_raw()
			x = acc['x']
			y = acc['y']
			z = acc['z']
			if (close(x,sequence[i][0],threshold) and close(y,sequence[i][1],threshold) and close(z,sequence[i][2],threshold)): # toutes les directions doivent etre bonnes
				i = advance(i)
			else:
				i = reset_display(sequence)
	if (i >= len(sequence)):
		unlocked_bool = True # pour sortir de la boucle quand la sequence à bien été reproduite

"""
	Affiche un cadenas déverrouiller et ensuite le message secret
"""
sense.set_pixels(unlocked)
sleep(2)
sense.show_message("Message", text_colour=[255, 0, 0])


