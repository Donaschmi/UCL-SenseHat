#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sense_hat import SenseHat, ACTION_RELEASED
from time import sleep
from math import log, exp
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

    for i in range(8):
        for j in range(8):
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

sense.stick.direction_left = pressed_left
sense.stick.direction_right = pressed_right

def create_temp_curve(temp_tab):
    global height, width
    def max_diff(arr, arr_size):
        max_diff = arr[1] - arr[0]
        for i in range( 0, arr_size  ):
            for j in range( i+1, arr_size  ):
                if(arr[j] - arr[i] > max_diff):
                    max_diff = arr[j] - arr[i]
        return max_diff

    sense.clear()
    # The max difference between two temp; if greater than 8, then we need to move vertically
    min_max_diff = max_diff(temp_tab, len(temp_tab))
    height = max(8, round(min_max_diff))

    width = len(temp_tab)
    print(width, height)
    # Create the full tab with every values
    #   height = max difference between two temp
    #   width = number of sample collected
    #
    #   Returns a height * width new tab
    temp_array = [[0 for x in range(height)] for y in range(width)]

    base_temp = temp_tab[0]
    base_index = 3

    for i in range(width):
        diff = round(temp_tab[i]) - round(base_temp)
        temp_array[i][base_index-diff] = 1
    print(temp_array)
    return temp_array


temp_raw, humid_raw = collect(10) # Will collect 10 samples
temp, humidex = treat_data(temp_raw, humid_raw)
print(temp)
full_tab = create_temp_curve(temp)
while True:
    # Continuously display the current tab while listening to joystick events
    display(current_display(full_tab))

