#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sense_hat import SenseHat, ACTION_RELEASED
from time import sleep
from math import log, exp
import sys
import subprocess

sense = SenseHat()

index_x = 0 # The current x-pos of the top_left pixel
index_y = 0 # The current y-pos of the top_left pixel
default_index_x = 0
default_index_y_temp = 0  # The default y-pos of the top_left pixel for the temperature tab; used to reset display
default_index_y_humid = 0 # The default y-pos of the top_left pixel for the humidity tab; used to reset display
height_temp = 8 # The maximum height the Temperature curve can have with a minimum of 8. [8, +infinity[
height_humid = 8 # The maximum height the Humidity curve can have with a minimum of 8. [8, +infinity[
width = 0 # Equals the number of samples collected

displayed_data = "humid"

def collect(number, time=0.5):
    """
    Collect data (temp, humid) over time and store it in array

    Parameters
    ----------
    number: int
        The number of samples to collect
    [time]: float
        The rate at which sample is collected in seconds

    Returns
    -------
    tab_temp: float[]
        Raw temperature collected
    tab_humid: float[]
        Raw humidity collected in percentages
    """
    tab_temp = [None] * number
    tab_humid = [None] * number
    for i in range(number):
        tab_temp[i] = sense.temperature
        tab_humid[i] = sense.humidity
        sleep(time) # Rate of collecting
    return (tab_temp, tab_humid)

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

    # Height depends on which data_set we have
    height = height_temp if displayed_data == "temp" else height_humid
    for i in range(min(8, width)):
        for j in range(min(8, height)):
            ret_tab[i][j] = tab[i + index_x][j + index_y]
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
        height = height_temp if displayed_data == "temp" else height_humid
        index_x = 0 if min(index_x + 1, width - 8) < 0 else min(index_x + 1, width - 8)
        print(index_x)

def pressed_up(event):
    global index_y
    if event.action != ACTION_RELEASED:
        index_y = max(0, index_y -1)
        print(index_y)

def pressed_down(event):
    global index_y
    if event.action != ACTION_RELEASED:
        height = height_temp if displayed_data == "temp" else height_humid
        index_y = 0 if min(index_y + 1, height - 8) < 0 else min(index_y + 1, height - 8)
        print(index_y)

def pressed_middle(event):
    global index_x, index_y, displayed_data
    if event.action != ACTION_RELEASED:
        if displayed_data == "temp":
            displayed_data = "humid"
            # Reset the index_y to the default index of the humid data_set
            index_y = default_index_y_humid
        else:
            displayed_data = "temp"
            # Reset the index_y to the default index of the temp data_set
            index_y = default_index_y_temp

# Mount the stick
sense.stick.direction_left = pressed_left
sense.stick.direction_right = pressed_right
sense.stick.direction_up = pressed_up
sense.stick.direction_down = pressed_down
sense.stick.direction_middle = pressed_middle

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
    global height_temp, height_humid, width, index_y, default_index_y_temp, default_index_y_humid

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
    min_max_diff = max_data - min_data

    full_data_tab = []

    width = len(data_tab)

    # We change our global variable accordingly to the displayed_data
    # Create the full tab with every values
    #   height = max difference between two temp
    #   width = number of sample collected
    #
    #   Returns a height * width new tab
    if displayed_data == "temp":
        height_temp = max(8, round(min_max_diff + 1))
        full_data_tab = [[0 for x in range(height_temp)] for y in range(width)]
    else:
        height_humid = max(8, round(min_max_diff + 1))
        full_data_tab = [[0 for x in range(height_humid)] for y in range(width)]

    # The first data that we collected is gonna be centered on the y-axis
    base_data = data_tab[0]

    # Change the base_index depending on max variation of temp
    base_index = round(max_data) - round(base_data)
    # Centers the base_index
    index_y = max(base_index - 4, 0)

    # Records value for when we change displayed_data
    if displayed_data == "temp":
        default_index_y_temp = index_y
    else:
        default_index_y_humid = index_y

    for i in range(width):
        diff = round(data_tab[i] - base_data)
        full_data_tab[i][base_index - diff] = 1
    return full_data_tab

temp = []
humid = []
if len(sys.argv) == 2:
    temp_raw, humid = collect(int(sys.argv[1]))
    temp = treat_data(temp_raw, humid)
elif len(sys.argv) == 3:
    temp_raw, humid = collect(int(sys.argv[1]), float(sys.argv[2]))
    temp = treat_data(temp_raw, humid)
else:
    # Dummy sample
    temp_raw = [23, 24, 25, 27, 27, 28, 29, 28, 28, 27, 27, 26, 25, 23, 33, 21, 21, 21, 20, 20, 19, 20, 21]
    humid = [60, 56, 51, 47, 44, 41, 38, 41, 41, 46, 49, 54, 60, 67, 68, 68, 70, 71, 73, 74, 75, 80, 79, 78]
    temp = treat_data(temp_raw, humid)

# Create both curves
full_humid_tab = create_curve(humid)
displayed_data = "temp"
full_temp_tab = create_curve(temp)

while True:
    # Continuously display the current tab while listening to joystick events
    current_tab = full_temp_tab if displayed_data == "temp" else full_humid_tab
    display(current_display(current_tab))
