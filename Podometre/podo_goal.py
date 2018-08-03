from sense_hat import SenseHat,ACTION_RELEASED,ACTION_PRESSED,ACTION_HELD
from time import sleep,time
from math import pow,sqrt, log, exp
from podo_display import display_number
import sys
import subprocess

# Setup
sense = SenseHat()
sense.low_light = True
temp_data = []
humid_data = []

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

cycle_time = time()
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

	if time() - cycle_time > 1:
		temp_data.append(sense.temp)
		humid_data.append(sense.humidity)
		cycle_time = time()

	sleep(0.018) # delay between 2 measures

# Clean before exit
sense.clear()
sense.set_pixels(Finished)
sleep(2)
index_x = 0 # The current x-pos of the top_left pixel
width = 0 # Equals the number of samples collected
prev_index = -1
displayed_data = "humid"

def humidex(temp, humid):
    """
    Converts the temperature into Humidex index according to its formula :
    https://en.wikipedia.org/wiki/Humidex

    Parameters
    ----------
    temp: float
        Temperature in Celcius degree
    humid: float
        Humidity in percentage

    Returns
    -------
    -: float
        The humidex index corresponding to temp and humid
    """
    a, b = 17.27, 237.7
    def alpha(temp, rh):
        return (a * temp) / (b + temp) + log(rh)

    def rosee(temp, rh):
        h = alpha(temp, rh)
        return (b * h) / (a - h)
    trash = (1. / 273.16) - (1. / (273.15 + rosee(temp, humid / 100)))
    e = 6.11 * exp(5417.7530 * trash)
    h = 0.5555 * (e - 10)
    return temp + h

def correct_temp(temp_tab):
    """
    Correct the temperature biased by the CPU temp

    Parameters
    ----------
    temp: float[]
        The collected temperature tab

    Returns
    -------
    temp_calibrated: float[]
        A more realistic temperature tab in Celcius degree
    """
    output = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True)
    cpu_temp = int(output)/1000
    temp_calibrated = [None] * len(temp_tab)
    for i in range(len(temp_tab)):
        temp_calibrated[i] = temp_tab[i] - ((cpu_temp - temp_tab[i]/1.5))
    return temp_calibrated

def treat_data(temp_tab, humid_tab):
    """
    Transform each temperature into humidex

    Parameters
    ----------
    temp_tab: float[]
        Temperature samples
    humid_tab: float[]
        Humidity samples

    Returns
    -------
    new_humidex: float[]
        New Humidex values
    """
    length = len(temp_tab)
    new_humidex = [None] * length
    new_temp_tab = correct_temp(temp_tab)
    for i in range(length):
        new_humidex[i] = humidex(new_temp_tab[i], humid_tab[i])
    return new_humidex

def display(tab):
    """
    Reads the temp_tab and set pixels accordingly

    Parameters
    ----------
    tab: int[][]
        A 8 * 8 length list containing either 0 or 1

    Returns
    -------
    -: /

    Display the current temp curve
    """
    screen = [None] * 64
    for i in range(8):
        for j in range(8):
            if tab[i][j] == 1:
                sense.set_pixel(i, j, 255, 0, 0) if displayed_data == "temp" else sense.set_pixel(i, j, 0, 0, 255)
            else:
                sense.set_pixel(i, j, 0, 0, 0)

def current_display(tab):
    """
    Adapt the temp tab accordingly to the current indexes

    Parameters
    ----------
    tab: int[][]
        A heihgt * width tab containing the entire curve

    Returns
    -------
    ret_tab: int [8][8]
        A 8 * 8 tab containing the pixels to display
    """
    ret_tab = [[0 for x in range(8)] for y in range(8)]

    for i in range(min(8, width)):
        for j in range(8):
            ret_tab[i][j] = tab[i + index_x][j]
    return ret_tab

def pressed_left(event):
    global index_x
    if event.action != ACTION_RELEASED:
        # We can't get behind index 0
        index_x = max(0, index_x - 1)
        print(index_x)

def pressed_right(event):
    global index_x
    if event.action != ACTION_RELEASED:
        # We can't get past the (8 - width) index or else we are out of boundary
        index_x = 0 if min(index_x + 1, width - 8) < 0 else min(index_x + 1, width - 8)
        print(index_x)

def pressed_middle(event):
    global index_x, displayed_data, state, debug
    if event.action == ACTION_RELEASED:
        if displayed_data == "temp":
            displayed_data = "humid"
        elif displayed_data == "humid":
            displayed_data = "temp"
        sense.clear()

def create_curve(data_tab):
    """
    Create a list of arrays where each array is a column containing exactly one "1"
    which is the the value at the index in data_tab

    Parameters
    ----------
    data_tab: float[]
        The data that will be drawn on the monitor

    Returns
    -------
    full_data_tab: int[][]
        Each list is a column of the full data array; [0,1]

    """
    global height_temp, height_humid, width, index_y, default_index_y_temp, default_index_y_humid, prev_index

    def min_max(arr, arr_size):
        """
        Helper to get the min and max of the tab
        """
        max_t = arr[0]
        min_t = arr[0]
        for i in range(arr_size):
            if arr[i] > max_t:
                max_t = arr[i]
            if arr[i] < min_t:
                min_t = arr[i]
        return min_t, max_t

    sense.clear()
    # The max difference between two temp; if greater than 8, then we need to move vertically
    min_data, max_data = min_max(data_tab, len(data_tab))
    min_max_diff = max(8, max_data - min_data)

    normalized_data = data_tab.copy()

    for i in range(len(data_tab)):
        normalized_data[i] = ((data_tab[i] - min_data)*7) / min_max_diff
    print(normalized_data)

    full_data_tab = []

    width = len(data_tab)

    full_data_tab = [[0 for x in range(8)] for y in range(width)]

    # The first data that we collected is gonna be centered on the y-axis
    base_data = normalized_data[0]

    # Change the base_index depending on max variation of temp
    base_index = 7 - round(base_data)

    # Records value for when we change displayed_data
    prev_index = -1
    for i in range(width):
        diff = round(normalized_data[i] - base_data)
        print(base_index, diff)
        curr_index = base_index - diff
        full_data_tab[i][curr_index] = 1

        # COMMENT NEXT FULL BLOCK TO REMOVE VERTICAL PIXELS
        if i > 0:
            delta_index = curr_index - prev_index
            print(delta_index)
            if delta_index > 1:
                for j in range(prev_index + 1, curr_index):
                    full_data_tab[i][j] = 1
            if delta_index < -1:
                for j in range(curr_index + 1, prev_index):
                    full_data_tab[i][j] = 1
        prev_index = curr_index
        # END OF BLOCK TO COMMENT


    return full_data_tab


humidex_data = treat_data(temp_data, humid_data)
full_humid_tab = create_curve(humid_data)
displayed_data = "temp"
full_temp_tab = create_curve(humidex_data)

# Mount the stick
sense.stick.direction_left = pressed_left
sense.stick.direction_right = pressed_right
sense.stick.direction_middle = pressed_middle

while True:
    # Continuously display the current tab while listening to joystick events
    if displayed_data == "temp":
        display(current_display(full_temp_tab))
    elif displayed_data == "humid":
        display(current_display(full_humid_tab))

print("Completed")
