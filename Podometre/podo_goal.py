from sense_hat import SenseHat,ACTION_RELEASED,ACTION_PRESSED,ACTION_HELD
from time import sleep,time
from math import pow,sqrt
from podo_display import display_number

# Setup
sense = SenseHat()
sense.low_light = True

ZERO = [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]]
ONE = [[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]]
TWO = [[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,1,1]]
THREE = [[1,1,1],[0,0,1],[1,1,1],[0,0,1],[1,1,1]]
FOUR = [[1,0,0],[1,0,1],[1,1,1],[0,0,1],[0,0,1]]
FIVE = [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]]
SIX = [[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]]
SEVEN = [[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,0,0]]
EIGHT = [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]]
NINE = [[1,1,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]]

NUMS = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]

ARROW = [[1, 1, 1],[0, 1, 0]]

index = 0
message = ""
coding = True
select = False

C = [255,0,0]

def display_number_2(number1, number2):
	for i in range(3):
		for j in range(5):
			sense.set_pixel(i+1, j+3, [255, 255, 255]) if number1[j][i] == 1 else sense.set_pixel(i+1, j+3, [0, 0, 0])
			sense.set_pixel(i+5, j+3, [255, 255, 255]) if number2[j][i] == 1 else sense.set_pixel(i+5, j+3, [0, 0, 0])
	offset = 0
	if index % 2 == 1:
		offset = 4
	for i in range(3):
		for j in range(2):
			sense.set_pixel(i+1+offset, j, [C[0], C[1], C[2]])if ARROW[j][i] == 1 else sense.set_pixel(i+1+offset, j, [0, 0, 0])

def pressed_right(event):
    global index
    if event.action != ACTION_PRESSED:
        index = (index + 1) % 10
        sense.clear()

def pressed_left(event):
    global index
    if event.action != ACTION_PRESSED:
        index = (index + 9) % 10
        sense.clear()

def pressed_middle(event):
	global coding,select
	if event.action == ACTION_RELEASED:
		global message
		message += str(index)
		select = True
		coding = False
		sleep(0.4)
		coding = True
		select = False
		print(message)
	elif event.action == ACTION_HELD:
		coding = False

def change_color():
	global index
	offset = 0
	if index % 2 == 1:
		offset = 4
	for i in range(3):
		for j in range(2):
			sense.set_pixel(i+1+offset, j, [100, 100, 200])if ARROW[j][i] == 1 else sense.set_pixel(i+1+offset, j, [0, 0, 0])


sense.stick.direction_right = pressed_right
sense.stick.direction_left = pressed_left
sense.stick.direction_middle = pressed_middle
sense.clear()
while True:
    if coding:
        display_number_2(NUMS[index], NUMS[index+1]) if index % 2 == 0 else display_number_2(NUMS[index - 1], NUMS[index])
    elif select:
    	change_color()
    elif not coding and not select:
        sense.show_message(message)
        break

message = message[:-1]

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
step_count = int(message) 		# TODO: import from select display LED

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
