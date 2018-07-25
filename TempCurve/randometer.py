#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sense_hat import SenseHat
from time import sleep
from math import log, exp
import subprocess

sense = SenseHat()

def collect(time):
    tab_temp = [None] * time
    tab_humid = [None] * time
    for i in range(time):
        tab_temp[i] = sense.temperature
        tab_humid[i] = sense.humidity / 100
        sleep(0.5)
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

def display(tab, w, h):
    screen = [None] * 64
    for i in range(w):
        for j in range(h):
            if tab[i][j] == 1:
                sense.set_pixel(i, j, 255, 0, 0)
            else:
                sense.set_pixel(i, j, 0, 0, 0)
def display_temp(temp_tab):

    def max_diff(arr, arr_size):
        max_diff = arr[1] - arr[0]
        for i in range( 0, arr_size  ):
            for j in range( i+1, arr_size  ):
                if(arr[j] - arr[i] > max_diff):
                    max_diff = arr[j] - arr[i]
        return max_diff

    sense.clear()
    min_max_diff = max_diff(temp_tab, len(temp_tab))
    height = max(8, round(min_max_diff))

    width = len(temp_tab)
    print(width, height)
    temp_array = [[0 for x in range(height)] for y in range(width)]

    base_temp = temp_tab[0]
    base_index = 3

    for i in range(width):
        diff = round(temp_tab[i]) - round(base_temp)
        temp_array[i][base_index-diff] = 1
    print(temp_array)
    display(temp_array, width, height)


temp_raw, humid_raw = collect(5)
temp, humidex = treat_data(temp_raw, humid_raw)
print(temp)
display_temp(temp)

