from sense_hat import SenseHat,ACTION_RELEASED, ACTION_HELD, ACTION_PRESSED
from time import sleep,time
from math import pow,sqrt, log, exp
import sys
import subprocess

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
B = [0, 0, 255]     # Blue color
O = [0,0,0]			# no Color

READY = [O,O,O,O,R,O,O,R,
        R,R,R,O,R,O,R,O,
        R,O,R,O,R,R,O,O,
        R,O,R,O,R,R,O,O,
        R,O,R,O,R,O,R,O,
        R,R,R,O,R,O,O,R,
        O,O,O,O,O,O,O,O,
        O,O,O,O,O,O,O,O] # 8x8 ok display


index_x = 0 # The current x-pos of the most left pixel
width = 0 # Equals the number of samples collected
prev_index = -1

# Default values, update at each loop
min_temp  = 99
max_temp = 0
min_humid  = 99
max_humid = 0

# 3 * 5 number representation
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

# Top indicator
H_MAX = [[O,B,O,B,O,O,B,O],
        [O,B,B,B,O,B,O,B],
        [O,B,O,B,O,O,O,O]]

H_MIN = [[O,B,O,B,O,B,O,B],
        [O,B,B,B,O,O,B,O],
        [O,B,O,B,O,O,O,O]]

T_MAX = [[O,R,R,R,O,O,R,O],
        [O,O,R,O,O,R,O,R],
        [O,O,R,O,O,O,O,O]]

T_MIN = [[O,R,R,R,O,R,O,R],
        [O,O,R,O,O,O,R,O],
        [O,O,R,O,O,O,O,O]]

PODO = [[O,O,G,O,O,G,O,O],
        [O,O,G,O,O,G,O,O],
        [O,O,G,G,O,G,G,O]]

# Different screens displayed
STATES = ["podo", "t_min", "t_max", "temp", "h_min", "h_max", "humid"]
index_state = 0 # Default is podo

TOP_DISPLAY = {"h_max": H_MAX, "h_min": H_MIN, "t_max": T_MAX, "t_min": T_MIN, "podo": PODO}


sense.set_pixels(READY) # display 'ok'

# Wait for any joystick event
event = sense.stick.wait_for_event()
event = sense.stick.wait_for_event()

sense.clear()

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
    temp_calibrated = temp_tab - ((cpu_temp - temp_tab)/1.5)
    return temp_calibrated

def treat_data(temp, humid):
    """
    Transform each temperature into humidex

    Parameters
    ----------
    temp_tab: float
        Temperature sample
    humid_tab: float
        Humidity sample

    Returns
    -------
    new_humidex: float
        New Humidex value
    """
    new_temp_tab = correct_temp(temp)
    new_humidex = humidex(new_temp_tab, humid)
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
                sense.set_pixel(i, j, 255, 0, 0) if STATES[index_state] == "temp" else sense.set_pixel(i, j, 0, 0, 255)
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

def pressed_right(event):
    global index_x
    if event.action != ACTION_RELEASED:
        # We can't get past the (8 - width) index or else we are out of boundary
        index_x = 0 if min(index_x + 1, width - 8) < 0 else min(index_x + 1, width - 8)

def pressed_middle(event):
    global index_x, index_state, loop
    if event.action == ACTION_RELEASED:
        index_state = (index_state + 1) % len(STATES)
        # Replace the display on the most recent data
        index_x = max(0, width - 8)
    sense.clear()

# Mount the stick
sense.stick.direction_left = pressed_left
sense.stick.direction_right = pressed_right
sense.stick.direction_middle = pressed_middle

def create_curve(data_tab, state):
    """
    Create a list of arrays where each array is a column containing exactly one "1"
    which is the the value at the index in data_tab

    Parameters
    ----------
    data_tab: float[]
        The data that will be drawn on the monitor
    state: String
        Either "temp" or "humid", specifies which data is beeing processed

    Returns
    -------
    full_data_tab: int[][]
        Each list is a column of the full data array; [0,1]

    """
    global width, prev_index, min_temp, max_temp, max_humid, min_humid

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

    # The max difference between two temp; if greater than 8, then we need to move vertically
    min_data, max_data = min_max(data_tab, len(data_tab))
    min_max_diff = max(8, max_data - min_data)

    # Update min/max values of each curve
    if state == "temp":
        min_temp = min(min_data, min_temp)
        max_temp = max(max_data, max_temp)
    elif state == "humid":
        min_humid = min(min_data, min_humid)
        max_humid = max(max_data, max_humid)

    width = len(data_tab)

    normalized_data = data_tab.copy()

    for i in range(len(data_tab)):
        normalized_data[i] = ((data_tab[i] - min_data)*7) / min_max_diff

    full_data_tab = [[0 for x in range(8)] for y in range(width)]

    # The first data that we collected is gonna be centered on the y-axis
    base_data = normalized_data[0]

    # Change the base_index depending on max variation of temp
    base_index = 7 - round(base_data)

    # Records value for when we change displayed_data
    prev_index = -1
    for i in range(width):
        diff = round(normalized_data[i] - base_data)
        curr_index = base_index - diff
        full_data_tab[i][curr_index] = 1

        # COMMENT NEXT FULL BLOCK TO REMOVE VERTICAL PIXELS
        if i > 0:
            delta_index = curr_index - prev_index
            if delta_index > 1:
                for j in range(prev_index + 1, curr_index):
                    full_data_tab[i][j] = 1
            if delta_index < -1:
                for j in range(curr_index + 1, prev_index):
                    full_data_tab[i][j] = 1
        prev_index = curr_index
        # END OF BLOCK TO COMMENT


    return full_data_tab

def display_number(number1, number2):
    """
    Display the two numbers on the 5 bottom lines of the screen and an
    indicator of which data is displayed

    Parameters
    ----------
    number1, number2: int[][]
        Valid 3*5 double_entry lists containing the number to display

    Returns
    -------
    /
    """
    top = TOP_DISPLAY[STATES[index_state]]
    ret_tab = [O]*64
    for i in range(8):
        for j in range(3):
            ret_tab[8 * j + i] = top[j][i]
    for i in range(3):
        for j in range(5):
            ret_tab[8 * (j+3) + i+1] = [255, 255, 255] if number1[j][i] == 1 else [0, 0, 0]
            ret_tab[8 * (j+3) + i+5] = [255, 255, 255] if number2[j][i] == 1 else [0, 0, 0]
    sense.set_pixels(ret_tab)

def main():
    # Contains  the data
    temp = []
    humid = []
    humidex_tab = []
    cycle_time = time()

    curve_temp = []
    curve_humid = []

    step_count = 0 		# Step counter
    prev_mag = 0.0 		# previous registered magnitude value
    prev_direction = 1 	# previous direction the data makes
    threshold = 1.37 	# Threshold value of magnitude
    # Main loop
    while True:

        acc = sense.get_accelerometer_raw() # read acc data
        x = acc['x']
        y = acc['y']
        z = acc['z']

        mag = sqrt(pow(x,2)+pow(y,2)+pow(z,2)) # Calculate magnitude

        cur_direction = direction(prev_mag,mag)# get current direction
        if cur_direction != prev_direction: # see if peak

            if (prev_direction == 1 and prev_mag > threshold): # check peak type (up,down) and if above some threshold
                step_count += 1
        # update variables
        prev_mag = mag
        prev_direction = cur_direction

        # Collect temp/humid every sec
        if time() - cycle_time > 1:
            temp.append(sense.temperature)
            humid.append(sense.humidity)
            humidex_tab.append(treat_data(temp[len(temp)-1], humid[len(humid)-1]))
            curve_humid = create_curve(humid, "humid")
            curve_temp = create_curve(humidex_tab, "temp")
            cycle_time = time()
        if STATES[index_state] == "h_max":
            display_number(NUMS[int(max_humid / 10)], NUMS[int(max_humid % 10)])
        elif STATES[index_state] == "h_min":
            display_number(NUMS[int(min_humid / 10)], NUMS[int(min_humid % 10)])
        elif STATES[index_state] == "t_max":
            display_number(NUMS[int(max_temp / 10)], NUMS[int(max_temp % 10)])
        elif STATES[index_state] == "t_min":
            display_number(NUMS[int(min_temp / 10)], NUMS[int(min_temp % 10)])
        elif STATES[index_state] == "podo":
            display_number(NUMS[int(step_count / 10)], NUMS[int(step_count % 10)])
        else:
            current_curve = curve_temp if STATES[index_state] == "temp" else curve_humid
            display(current_display(current_curve))

        sleep(0.018) # delay between 2 measures

main()
