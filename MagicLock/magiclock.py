#!/usr/bin/env python3
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_RELEASED, ACTION_HELD
import os.path
import json
import ast
import sys
from time import sleep, time
from math import floor
# Indicate which combinaison is currently beeing tried
code_index = 0

# Define the combinaisons variable as a list of element (dict or int)
code_combinaison = [None]*64

# Number of combinaisons
code_num = 0

# Our secret message
message = ""

state = ""

tries = 0

# Color code
R = [255, 0, 0]
G = [127, 255, 0]
B = [0, 0, 255]
O = [255, 255, 255]

# Some image to display
locked=[O,O,O,O,O,O,O,O,
        O,O,R,R,R,R,O,O,
        O,O,R,O,O,R,O,O,
        O,O,R,O,O,R,O,O,
        O,R,R,R,R,R,R,O,
        O,R,R,R,R,R,R,O,
        O,R,R,R,R,R,R,O,
        O,R,R,R,R,R,R,O]

unlocked=[O,O,G,G,G,G,O,O,
        O,O,G,O,O,G,O,O,
        O,O,G,O,O,G,O,O,
        O,O,O,O,O,G,O,O,
        O,G,G,G,G,G,G,O,
        O,G,G,G,G,G,G,O,
        O,G,G,G,G,G,G,O,
        O,G,G,G,G,G,G,O]

question_mark=[O,O,O,B,B,B,O,O,
        O,O,B,B,B,B,B,O,
        O,B,B,O,O,B,B,O,
        O,O,O,O,O,B,B,O,
        O,O,O,O,B,B,O,O,
        O,O,O,B,B,O,O,O,
        O,O,O,O,O,O,O,O,
        O,O,O,B,B,O,O,O]

wrong = [O,O,R,R,R,R,O,O,
        O,R,O,O,O,O,R,O,
        R,O,R,O,O,O,O,R,
        R,O,O,R,O,O,O,R,
        R,O,O,O,R,O,O,R,
        R,O,O,O,O,R,O,R,
        O,R,O,O,O,O,R,O,
        O,O,R,R,R,R,O,O]

finished = 	[O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,O,
			O,O,O,O,O,O,O,G,
			O,O,O,O,O,O,G,G,
			O,G,O,O,O,G,O,G,
			O,O,G,O,G,O,O,O,
			O,O,O,G,O,O,O,O,
			O,O,O,O,O,O,O,O]

# The default display screen
display = [O] * 64

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

coding = True

select = False

debug = True

# Setup SenseHat
sense = SenseHat()
sense.low_light = True
sense.clear()
def close_enough(x, value):
    """
    Checks if the current value is close enough to x

    Parameters
    ----------
    x: float
        The value we want to compare to
    value: float
        The value we want to compare

    Returns
    -------
    -: bool
        True if value is close enough to x with a threshold factor of 0.12, else False
    """
    threshold = 0.12
    return  x >= (value - threshold) and x <= (value + threshold)

def find_direction(acc):
    x = round(acc['x'])
    y = round(acc['y'])
    z = round(acc['z'])

    # Print the color only to help to locate them on the RPI, should be removed once deployed
    if x == 1 and y == 0 and z == 0:
        print("red")
        return 5
    elif x == -1 and y == 0 and z == 0:
        print("blue")
        return 6
    elif x == 0 and y == 1 and z == 0:
        print("green")
        return 7
    elif x == 0 and y == -1 and z == 0:
        print("yellow")
        return 8
    elif x == 0 and y == 0 and z == 1:
        print("orange")
        return 9
    elif x == 0 and y == 0 and z == -1:
        print("grey")
        return 10
    else:
        return 11


def isValid(secret_file):
    """
    Checks if the secret_file given is of a valid form

    The secret_file should contain len(file) - 1 lines containing either a dictionnary or an integer
    and a one line message before the EOF.

    Fill the global code_combinaison with the lines contained in the secret_file
    Fill the global message with the last line of the secret_file

    Parameters
    ----------
    secret_file: File
        An opened secret_file in reading mode

    Returns
    -------
    -:bool
        True if each line of the secret_file except the last one is either a dictionnary or an integer,
        else False
    """
    global code_combinaison, code_index, code_num, message
    # Contains each line of the secret_file
    lines = secret_file.read().split('\n')

    code_num = len(lines) - 1
    code_combinaison = [None] * code_num

    # For each line in lines
    for i in range(code_num):
        if not lines[i].isdigit():
            return False
        else: # Line is a number
            if int(lines[i]) < 1 or int(lines[i]) > 10:
                return False
            code_combinaison[code_index] = int(lines[i])

        code_index += 1

    # Reset the counter
    code_index = 0

    message = lines[len(lines) - 1]
    return True

def translate(number):
    """
    Translate the number into a direction

    1 : up
    2 : down
    3 : left
    4 : right

    Parameters
    ----------
    number:int
        The direction number

    Returns
    -------
    -: String
        The corresponding direction or "up" if (number > 4) or (number < 1)
    """
    if number == 1:
        return "up"
    elif number == 2:
        return "down"
    elif number == 3:
        return "left"
    elif number == 4:
        return "right"
    else:
        return "up"

def reset_display():
    """
    Reset the display if a combinaison is wrong and returns the 0, the next counter index

    Parameters
    ----------
    /

    Returns
    -------
    -: int
        Returns 0
    """
    global tries
    tries += 1
    if tries > 5:
        sense.set_pixels(wrong)
        sleep(1)
        sense.clear()
        sys.exit(1)
    for i in range(code_num):
        display[i] = R
    sense.set_pixels(display)
    return 0

def advance(i):
    """
    Called when a combinaison is correct, fill a red pixel with green, increment the counter

    Parameters
    ----------
    i: int
        The current counter index

    Returns
    -------
    p: int
        i + 1
    """
    display[i] = G
    sense.set_pixels(display)
    p = i + 1
    print("Bravo! (%s/%s)"%(str(p), str(len(code_combinaison))))
    return p

def decrypt(secret_file):
    """
    Main function for decryption

    Will wait for event to occure and compare them with the expected event stored in code_combinaison
    The user will unlock the locks step by step unless he makes a mistake and has to start over

    Parameters
    ----------
    secret_file: File
        The secret_file containing the combinaison and the message

    Returns
    -------
    /
    """
    global code_index, code_combinaison, code_num,  message, locked, unlocked

    sense.set_pixels(locked)

    # Wait for an event in order to begin
    print("Appuyer sur le joystick pour déverrouiller")
    event = sense.stick.wait_for_event()
    while event.action != ACTION_RELEASED:
        event = sense.stick.wait_for_event()

    sense.stick.direction_middle = pushed_middle_de
    sense.stick.direction_up = pushed_up_de
    sense.stick.direction_down = pushed_down_de
    sense.stick.direction_right = pushed_right_de
    sense.stick.direction_left = pushed_left_de

    if code_num == 0:
        sense.set_pixels(unlocked)
        sleep(2)
        sense.show_message(message)
        return
    sense.clear()
    # Display the number of locks, the red are the locked ones and the green the unlocked
    for i in range(code_num):
        display[i] = R
    sense.set_pixels(display)
    sense.set_imu_config(False, False, True) # active seulement l'accelerometre

    locked = True
    print("Pivoter puis valider la position ou diriger le joystick dans une direction")
    while locked:
        # If their are no more locked locks
        if code_index >= len(code_combinaison):
            locked = False

    sense.set_pixels(unlocked)
    sleep(2)
    sense.show_message(message)


def display_code_index():
        """
        Function that increases the code_index variable and illuminates this amount of leds on the panel
        """
        sense.clear()
        for i in range(code_index):
            x = i % 8; # get column index
            y = i / 8; # get row index
            sense.set_pixel(int(floor(x)),int(floor(y)),100,100,200) # set pixel to blue

def change_color():
        """
        Function that changes the cursor color from red to blue.
        This function is called when the user selects a digit form the numberpicker
        """
        global index
        offset = 0
        if index % 2 == 1:
            offset = 4
        for i in range(3):
            for j in range(2):
                sense.set_pixel(i+1+offset, j, [100, 100, 200])if ARROW[j][i] == 1 else sense.set_pixel(i+1+offset, j, [0, 0, 0])

"""
The following 4 functions are used in encryption mode

When a joystick action other than the middle one occure, save it and increment the index

1 : up
2 : down
3 : left
4 : right
"""

def pushed_up_en(event):
    if state == "typing":
        pass
    else:
        global code_index, code_combinaison
        if event.action == ACTION_RELEASED:
            code_combinaison[code_index] = 1
            code_index += 1
            display_code_index()

def pushed_down_en(event):
    if state == "typing":
        pass
    else:
        global code_index, code_combinaison
        if event.action == ACTION_RELEASED:
            code_combinaison[code_index] = 2
            code_index += 1
            display_code_index()

def pushed_left_en(event):
    if state == "typing":
        global index
        if event.action != ACTION_PRESSED:
            index = (index + 9) % 10
            sense.clear()
    else:
        global code_index, code_combinaison
        if event.action == ACTION_RELEASED:
            code_combinaison[code_index] = 3
            code_index += 1
            display_code_index()

def pushed_right_en(event):
    if state == "typing":
        global index
        if event.action != ACTION_PRESSED:
            index = (index + 1) % 10
            sense.clear()
    else:
        global code_index, code_combinaison
        if event.action == ACTION_RELEASED:
            code_combinaison[code_index] = 4
            code_index += 1
            display_code_index()

def pushed_middle_en(event):
    global message, state, code_index, code_combinaison, debug, index, select
    if state == "typing":
        if event.action == ACTION_RELEASED:
            message += str(index)
            select = True
            sleep(0.3) # time the cursor will be blue (select mode)
            select = False
        elif event.action == ACTION_HELD:
            state = "coding"
            sleep(2)

    elif state == "coding":
        if event.action == ACTION_PRESSED:
            debug = False
        if event.action == ACTION_RELEASED and not debug:
            acc = sense.get_accelerometer_raw()
            direction = find_direction(acc)
            if direction == 11:
                sense.set_pixels(wrong)
                sleep(1)
                sense.clear()
                display_code_index()
                return

            code_combinaison[code_index] = direction
            code_index += 1
            display_code_index()
        elif event.action == ACTION_HELD and not debug:
            state = "done"

def pushed_up_de(event):
    global code_index
    if event.action == ACTION_RELEASED:
        if code_combinaison[code_index] == 1:
            code_index = advance(code_index)
        else:
            code_index = reset_display()

def pushed_down_de(event):
    global code_index
    if event.action == ACTION_RELEASED:
        if code_combinaison[code_index] == 2:
            code_index = advance(code_index)
        else:
            code_index = reset_display()

def pushed_left_de(event):
    global code_index
    if event.action == ACTION_RELEASED:
        if code_combinaison[code_index] == 3:
            code_index = advance(code_index)
        else:
            code_index = reset_display()

def pushed_right_de(event):
    global code_index
    if event.action == ACTION_RELEASED:
        if code_combinaison[code_index] == 4:
            code_index = advance(code_index)
        else:
            code_index = reset_display()

def pushed_middle_de(event):
    global code_index
    if event.action == ACTION_RELEASED:
        acc = sense.get_accelerometer_raw()
        if find_direction(acc) == code_combinaison[code_index]:
            code_index = advance(code_index)
        else:
            code_index = reset_display()


def display_number(number1, number2):
    for i in range(3):
        for j in range(5):
            sense.set_pixel(i+1, j+3, [255, 255, 255]) if number1[j][i] == 1 else sense.set_pixel(i+1, j+3, [0, 0, 0])
            sense.set_pixel(i+5, j+3, [255, 255, 255]) if number2[j][i] == 1 else sense.set_pixel(i+5, j+3, [0, 0, 0])
    offset = 0
    if index % 2 == 1:
        offset = 4
    for i in range(3):
        for j in range(2):
            sense.set_pixel(i+1+offset, j, [255, 0, 0])if ARROW[j][i] == 1 else sense.set_pixel(i+1+offset, j, [0, 0, 0])


def encrypt(secret_file):
    """
    Records actions performed and a message and save it in the secret_file

    Parameters
    ----------
    secret_file: File
        The secret file containing the locks and the message

    Returns
    -------
    /
    """
    global code_combinaison

    # Wait for the message to be entered
    while state == "coding":
        pass
    for i in range(len(code_combinaison)):
        if not code_combinaison[i] is None:
            secret_file.write(str(code_combinaison[i])+ '\n')
    secret_file.write(str(message))

if os.path.isfile("secretKey.txt"):
    secret_file = open("secretKey.txt", "r")
    if isValid(secret_file):
        state = "decrypt"
        decrypt(secret_file)

else:
    secret_file = open("secretKey.txt", "w")
    state = "typing"
    # Bind the joystick actions
    sense.stick.direction_middle = pushed_middle_en
    sense.stick.direction_up = pushed_up_en
    sense.stick.direction_down = pushed_down_en
    sense.stick.direction_right = pushed_right_en
    sense.stick.direction_left = pushed_left_en
    while state == "typing":
        if select: # if the user has selected a number, change the cursor color
        	change_color()
        else:
        	display_number(NUMS[index], NUMS[index+1]) if index % 2 == 0 else display_number(NUMS[index - 1], NUMS[index])

    sense.show_message(message)
    #sense.show_message("Pivotez et validez vos positions et/ou diriger le joystick", scroll_speed=0.05)
    sense.set_pixels(question_mark)
    encrypt(secret_file)
    secret_file.close()
    sense.set_pixels(finished)
    sleep(1)
    sense.clear()
