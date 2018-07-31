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

def direction(previous_elem, element):
	if (previous_elem > element):
		return -1 # descending direction
	else:
		return 1



# Variables
R = [255, 0, 0]
G = [127, 255, 0]
step_count = 0
data = []
prev_mag = 0.0
cur_direction = 1
prev_direction = 1
threshold = 1.40
infinite = True


# display red screen to show start of logging
display = [G] * 64
sense.set_pixels(display)
start_time = current_milli_time()
display_number(0)


def stop():
	global infinite
	infinite = 0

# set stop action by touching the joystick
sense.stick.direction_any = stop

# infinite loop, stopped on any joystick move
while infinite:

	t = current_milli_time()
	acc = sense.get_accelerometer_raw()
	x = acc['x']
	y = acc['y']
	z = acc['z']
	data.append((x,y,z)) # append new data point !! RAM costely
	
	mag = sqrt(pow(x,2)+pow(y,2)+pow(z,2)) # Calculate magnitude
	
	if direction(prev_mag,mag) != prev_direction: # see if peak or not
		# peak because we descend now is previous value is peak!

		if (prev_direction == 1 and prev_mag > threshold): # check if above some threshold
			step_count += 1
			display_number(step_count)
	
	# update variables	
	prev_mag = mag
	prev_direction = cur_direction
	
	
	sleep(0.018) # delay between 2 measures
	
	#if (t-start_time > 11000):
	#	break


# Clean before exit
sense.clear()
print(str(step_count))
display_number(step_count)

	
