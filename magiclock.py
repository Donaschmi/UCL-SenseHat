#!/usr/bin/env python3
from sense_emu import SenseHat, ACTION_PRESSED, ACTION_RELEASED, ACTION_HELD
import os.path
import json
import ast
from time import sleep

code_index = 0
code_combinaison = [None]*64
code_num = 0

message = ""

R = [255, 0, 0]
G = [127, 255, 0]
O = [255, 255, 255]

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


display = [O] * 64

sense = SenseHat()
sense.low_light = True

def close(x, value):
    threshold = 0.12
    return  x > (value - threshold) and x < (value + threshold)


def isValid(fichier):
    global code_combinaison, code_index, code_num, message
    line = fichier.read().split('\n')
    code_num = len(line) - 1
    code_combinaison = [None] * code_num
    for i in range(code_num):
        if not line[i].isdigit():
            h = ast.literal_eval(line[i])
            if type(h) is dict:
                code_combinaison[code_index]= h
            else:
                print(line[i])
                return False
        else:
            code_combinaison[code_index] = int(line[i])
        code_index += 1
    code_index = 0
    message = line[len(line) - 1]
    return True

def translate(number):
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
    for i in range(code_num):
        display[i] = R
    sense.set_pixels(display)
    return 0

def advance(i):
    display[i] = G
    sense.set_pixels(display)
    p = i + 1
    print("Bravo! (%s/%s)"%(str(p), str(len(code_combinaison))))
    return p

def decrypt(fichier):
    global code_index, code_combinaison, code_num,  message, locked, unlocked

    sense.set_pixels(locked)
    print("Appuyer sur le joystick pour déverrouiller")
    event = sense.stick.wait_for_event()
    while event.action != ACTION_RELEASED:
        event = sense.stick.wait_for_event()


    for i in range(code_num):
        display[i] = R
    sense.set_pixels(display)
    sense.set_imu_config(False, False, True) # active seulement l'accelerometre
    locked = True
    print("Pivoter puis valider la position ou diriger le joystick dans une direction")
    while locked:
        event = sense.stick.wait_for_event()
        if event.action == ACTION_PRESSED:
            if event.direction != "middle":
                if (not type(code_combinaison[code_index]) is dict) and (translate(code_combinaison[code_index]) == event.direction):
                    code_index = advance(code_index)
                else:
                    code_index = reset_display()
            else:
                if not type(code_combinaison[code_index]) is dict:
                    code_index = reset_display()
                    continue

                acc = sense.get_accelerometer_raw()
                x = acc['x']
                y = acc['y']
                z = acc['z']
                if (close(x,code_combinaison[code_index]['x'])
                        and close(y,code_combinaison[code_index]['y'])
                        and close(z,code_combinaison[code_index]['z'])): # toutes les directions doivent etre bonnes
                    code_index = advance(code_index)
                else:
                	code_index = reset_display()
        if code_index >= len(code_combinaison):
            locked = False
    sense.set_pixels(unlocked)
    sleep(2)
    sense.show_message(message)

def pushed_middle(event):
    global code_index, code_combinaison
    if event.action == ACTION_PRESSED:
        code_combinaison[code_index] = sense.get_accelerometer_raw()
        code_index += 1

def pushed_up(event):
    global code_index, code_combinaison
    if event.action == ACTION_PRESSED:
        code_combinaison[code_index] = 1
        code_index +=1

def pushed_down(event):
    global code_index, code_combinaison
    if event.action == ACTION_PRESSED:
        code_combinaison[code_index] = 2
        code_index +=1

def pushed_left(event):
    global code_index, code_combinaison
    if event.action == ACTION_PRESSED:
        code_combinaison[code_index] = 3
        code_index +=1

def pushed_right(event):
    global code_index, code_combinaison
    if event.action == ACTION_PRESSED:
        code_combinaison[code_index] = 4
        code_index +=1

def encrypt(fichier):
    global code_combinaison

    message = input("Entrez votre message secret : \n")
    for i in range(len(code_combinaison)):
        if not code_combinaison[i] is None:
            fichier.write(str(code_combinaison[i])+ '\n')
    fichier.write(str(message))

if os.path.isfile("secretKey.txt"):
    fichier = open("secretKey.txt", "r")
    if isValid(fichier):
        decrypt(fichier)
else:
    fichier = open("secretKey.txt", "w")

    print("Pencher puis valider les position en appuyant sur le joystick ou pousser le joystick dans une direction (5 positions à données)")
    sense.stick.direction_middle = pushed_middle
    sense.stick.direction_up = pushed_up
    sense.stick.direction_down = pushed_down
    sense.stick.direction_right = pushed_right
    sense.stick.direction_left = pushed_left
    encrypt(fichier)
    fichier.close()
