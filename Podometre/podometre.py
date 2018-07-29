from sense_hat import SenseHat,ACTION_RELEASED
from time import sleep,time
from math import pow,sqrt
from podo_display import display_number

# Setup
sense = SenseHat()
sense.low_light = True


# Fonction qui renvoie le temps en ms
current_milli_time = lambda: int(round(time() * 1000))

start_time = current_milli_time()

# Variables
R = [255, 0, 0]
G = [127, 255, 0]
mean = 0.0
step_count = 0
data = []
prev = 0

# display red screen to show inactivity
display = [R] * 64
sense.set_pixels(display)

# Wait for an event in order to begin
#print("Appuyer sur le joystick pour commencer")
#event = sense.stick.wait_for_event()
#while event.action != ACTION_RELEASED:
#	event = sense.stick.wait_for_event()


# display red screen to show start of logging
display = [G] * 64
sense.set_pixels(display)
start_time = current_milli_time()
display_number(0)
infinite = True 

def stop():
	global infinite
	infinite = False

# set stop action by touching the joystick
sense.stick.direction_any = stop

# infinite loop
# TODO: stop loop on joystick press?
while infinite:

	t = current_milli_time()
	acc = sense.get_accelerometer_raw()
	x = acc['x']
	y = acc['y']
	z = acc['z']
	data.append((x,y,z)) # append new data point
	
	mag = sqrt(pow(x,2)+pow(y,2)+pow(z,2)) # Calculate magnitude
	
	
	if (mag > 1.3):
		step_count += 1
		display_number(step_count)
	
	sleep(0.018) # gogo
	
	# stop after 10 seconds
	#if (t-start_time > 10000):
	#	break


# Clean before exit
sense.clear()
print(str(step_count))



"""

"""




	
