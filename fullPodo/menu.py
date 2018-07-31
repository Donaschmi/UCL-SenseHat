#!/usr/bin/env python3

from sense_hat import SenseHat, ACTION_RELEASED
import subprocess

sense = SenseHat()

Br = [128,0,0] 
R = [255,0,0]
Bl = [130,50,0]
X = [0,0,0]
Or = [255,140,0]
P = [150,150,150]

Temp = [X,X,X,X,X,X,X,X,
		X,Bl,Bl,Bl,Bl,Bl,Bl,X,
		X,X,X,Bl,Bl,X,X,X,
		X,X,X,Bl,Bl,X,X,X,
		X,X,X,Bl,Bl,X,X,X,
		X,X,X,Bl,Bl,X,X,X,
		X,X,X,Bl,Bl,X,X,X,
		X,X,X,Bl,Bl,X,X,X]

Podo = [Or,Or,Or,Or,Or,Or,Or,Or,
		Or,Or,Or,Or,Or,Or,Or,Or,
		X,Or,X,X,X,X,Or,X,
		X,Or,X,X,X,X,Or,X,
		X,Or,X,X,X,X,Or,X,
		X,R,R,X,X,X,R,R,
		X,R,R,R,X,X,R,R,
		X,X,X,X,X,X,X,X]
		
Hum = 	[X,X,X,X,X,X,X,X,
		X,Bl,X,X,X,X,Bl,X,
		X,Bl,X,X,X,X,Bl,X,
		X,Bl,X,X,X,X,Bl,X,
		X,Bl,Bl,Bl,Bl,Bl,Bl,X,
		X,Bl,X,X,X,X,Bl,X,
		X,Bl,X,X,X,X,Bl,X,
		X,Bl,X,X,X,X,Bl,X]

menu = {0:Temp, 1:Podo, 2:Hum}

sense.set_pixels(Temp)

cursor = 0

"""
Function used when update led needed
"""
def update_led(event):
	global cursor
	if event.action != ACTION_RELEASED:
		sense.set_pixels(menu[cursor])
	print("defegr")

"""
Function used when joystick pressed right
"""
def right(event):
	global cursor
	if event.action != ACTION_RELEASED:
		cursor = ((cursor+1) % 3)

"""
Function used when joystick pressed left
"""
def left(event):
	global cursor
	if event.action != ACTION_RELEASED:
		cursor = ((cursor-1) % 3)

"""
Function called on selection of item in menu
"""
def select(event):
	global cursor
	if event.action != ACTION_RELEASED:
		if cursor == 0:
			# launch Temp
			print("Temp selected")
			sense.clear()
		elif cursor == 1:
			# launch Podometer
			print("Podo selected")
			sense.clear()
			subprocess.run(["python3", "podometre.py"])
		elif cursor == 2:
			# launch Humiddity
			print("Humidity selected")
			sense.clear()
		else:
			pass
	print("Done")

"""
Function to get back to the menu
"""
def back(event):
	global cursor
	if event.action != ACTION_RELEASED:
		cursor = 0
		print("Back to menu")

# Link joystick and functions
sense.stick.direction_left = left
sense.stick.direction_right = right
sense.stick.direction_any = update_led
sense.stick.direction_middle = select
sense.stick.direction_up = back
sense.stick.direction_down = back


# Avoid stop script
while True:
	pass
