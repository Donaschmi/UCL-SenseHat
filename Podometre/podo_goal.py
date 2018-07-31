from sense_hat import SenseHat,ACTION_RELEASED
from time import sleep,time
from math import pow,sqrt
from podo_display import display_number

# Setup
sense = SenseHat()
sense.low_light = True

"""
Function that returns 1 if previous_elem <= element else -1
"""
def direction(previous_elem, element):
	if (previous_elem > element):
		return -1 # descending direction
	else:
		return 1

"""
Function that sets the loop condition to false
"""
def stop():
	global infinite
	infinite = 0


# Colors
R = [255, 0, 0]		# Red
G = [127, 255, 0]	# Green
X = [0,0,0]			# None
step_count = 5 		# TODO: import from select display LED

Finished = 	[X,X,X,X,X,X,X,X,
			X,X,X,X,X,X,X,X,
			X,X,X,X,X,X,X,G,
			X,X,X,X,X,X,G,G,
			X,G,X,X,X,G,X,G,
			X,X,G,X,G,X,X,X,
			X,X,X,G,X,X,X,X,
			X,X,X,X,X,X,X,X]


prev_mag = 0.0		# Previous magnitude value
prev_direction = 1	# Previous direction value
threshold = 1.37	# threshold value: if mag > => then step++
infinite = True		# condition of main loop


# display step_count at start
display_number(step_count)

# set stop action by touching the joystick
sense.stick.direction_any = stop

# infinite loop, stopped on any joystick move
while infinite:

	acc = sense.get_accelerometer_raw()
	x = acc['x']
	y = acc['y']
	z = acc['z']
	
	mag = sqrt(pow(x,2)+pow(y,2)+pow(z,2)) # Calculate magnitude
	
	cur_direction = direction(prev_mag,mag)
	if cur_direction != prev_direction: # see if peak

		if (prev_direction == 1 and prev_mag > threshold): # check if above some threshold and previous direction was up
			step_count -= 1
			display_number(step_count)
	
	if (step_count <= 0):
		break
	# update variables	
	prev_mag = mag
	prev_direction = cur_direction
	
	sleep(0.018) # delay between 2 measures

# Clean before exit
sense.clear()
sense.set_pixels(Finished)
print("Completed")	
