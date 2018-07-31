from sense_hat import SenseHat, ACTION_PRESSED, ACTION_RELEASED, ACTION_HELD

sense = SenseHat()

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
    if event.action == ACTION_RELEASED:
        global message
        message += str(index)
        print(message)
    elif event.action == ACTION_HELD:
        global coding
        coding = False

sense.stick.direction_right = pressed_right
sense.stick.direction_left = pressed_left
sense.stick.direction_middle = pressed_middle
sense.clear()
while True:
    if coding:
        display_number(NUMS[index], NUMS[index+1]) if index % 2 == 0 else display_number(NUMS[index - 1], NUMS[index])
    else:
        sense.show_message(message)
        break
