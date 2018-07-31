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



R = [255, 0, 0] 	# Red color
G = [127, 255, 0] 	# Green color
X = [0,0,0]			# no Color
Ready = [X,X,X,X,R,X,X,R,
		R,R,R,X,R,X,R,X,
		R,X,R,X,R,R,X,X,
		R,X,R,X,R,R,X,X,
		R,X,R,X,R,X,R,X,
		R,R,R,X,R,X,X,R,
		X,X,X,X,X,X,X,X,
		X,X,X,X,X,X,X,X] # 8x8 ok display

step_count = 0 		# Step counter
prev_mag = 0.0 		# previous registered magnitude value
prev_direction = 1 	# previous direction the data makes
threshold = 1.40 	# Threshold value of magnitude
loop = True 		# Boolean variable for loop

sense.set_pixels(Ready) # display 'ok'

# Wait for any joystick event
event = sense.stick.wait_for_event()
event = sense.stick.wait_for_event()

sense.clear()

"""
Sets the global variable loop to False
"""
def stop():
	global loop
	loop = False

# set stop action by touching the joystick
sense.stick.direction_any = stop

# display 00 at start
display_number(0)

# Main loop
while loop:

	acc = sense.get_accelerometer_raw() # read acc data
	x = acc['x']
	y = acc['y']
	z = acc['z']
	
	mag = sqrt(pow(x,2)+pow(y,2)+pow(z,2)) # Calculate magnitude
	
	cur_direction = direction(prev_mag,mag)# get current direction
	if cur_direction != prev_direction: # see if peak

		if (prev_direction == 1 and prev_mag > threshold): # check peak type (up,down) and if above some threshold
			step_count += 1
			display_number(step_count) # update number on screen
	
	# update variables	
	prev_mag = mag
	prev_direction = cur_direction
	
	
	sleep(0.018) # delay between 2 measures

# Clean before exit
sense.clear()
print(str(step_count))
display_number(step_count)

	
