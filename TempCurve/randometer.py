#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sense_hat import SenseHat, ACTION_RELEASED
from time import sleep
from math import log, exp
import sys
import subprocess

sense = SenseHat()

index_x = 0
index_y = 0
height = 0
width= 0

def collect(time):
    tab_temp = [None] * time
    tab_humid = [None] * time
    for i in range(time):
        tab_temp[i] = sense.temperature
        tab_humid[i] = sense.humidity / 100
        sleep(0.5) # Rate of collecting
    return (tab_temp, tab_humid)

def humidex(temp, humid):
    a, b = 17.27, 237.7
    def alpha(temp, rh):
        return (a * temp) / (b + temp) + log(rh)

    def rosee(temp, rh):
        h = alpha(temp, rh)
        return (b * h) / (a - h)
    trash = (1. / 273.16) - (1. / (273.15 + rosee(temp, humid)))
    e = 6.11 * exp(5417.7530 * trash)
    h = 0.5555 * (e - 10)
    return temp + h

def correct_temp(temp):
    output = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True)
    cpu_temp = int(output)/1000
    temp_calibrated = temp - ((cpu_temp - temp)/1.5)
    return temp_calibrated

def treat_data(tab_temp, tab_humid):
    length = len(tab_temp)
    new_temp = [None] * length
    new_humid = [None] * length
    for i in range(length):
        new_temp[i] = correct_temp(tab_temp[i])

        new_humid[i] = humidex(new_temp[i], tab_humid[i])
    return new_temp, new_humid

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
                sense.set_pixel(i, j, 255, 0, 0)
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
        index_y = 0 if min(index_y + 1, height - 8) < 0 else min(index_y + 1, height - 8)
        print(index_y)

sense.stick.direction_left = pressed_left
sense.stick.direction_right = pressed_right
sense.stick.direction_up = pressed_up
sense.stick.direction_down = pressed_down

def create_temp_curve(temp_tab):
    global height, width, index_y

    def min_max(arr, arr_size):
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
    min_t, max_t = min_max(temp_tab, len(temp_tab))
    min_max_diff = max_t - min_t
    print(temp_tab)
    height = max(8, round(min_max_diff+1))

    width = len(temp_tab)
    # Create the full tab with every values
    #   height = max difference between two temp
    #   width = number of sample collected
    #
    #   Returns a height * width new tab
    temp_array = [[0 for x in range(height)] for y in range(width)]
    print(temp_array)

    base_temp = temp_tab[0]

    # Change the base_index depending on max variation of temp
    # eg : If at t=10 the temp is at its maximum,
    base_index = round(max_t) - round(base_temp)
    print(base_index)

    index_y = base_index - 4
    print("index_y = ", index_y)
    for i in range(width):
        diff = round(temp_tab[i]) - round(base_temp)
        print(base_index - diff)
        temp_array[i][base_index - diff] = 1
    print(temp_array)
    return temp_array

tab = []
if len(sys.argv) > 1:
    temp_raw, humid_raw = collect(int(sys.argv[1]))
    tab, humid = treat_data(temp_raw, humid_raw)
else:
    tab = [26, 25, 24, 23, 22, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
full_tab = create_temp_curve(tab)

# Debugging purpose

while True:
    # Continuously display the current tab while listening to joystick events
    display(current_display(full_tab))
