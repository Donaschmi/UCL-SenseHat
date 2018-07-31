from sense_hat import SenseHat
from math import floor
## display 2 digit values as step counter
C = [255,0,0] # color for digits
X = None # no color

zero =	[C, C, C,
		C, X, C,
		C, X, C,
		C, X, C,
		C, C, C]
one = 	[X, C, X,
		C, C, X,
		X, C, X,
		X, C, X,
		C, C, C]
two = 	[C, C, C,
		X, X, C,
		C, C, C,
		C, X, X,
		C, C, C]
three = [C, C, C,
		X, X, C,
		C, C, C,
		X, X, C,
		C, C, C]
four = 	[C, X, X,
		C, X, C,
		C, C, C,
		X, X, C,
		X, X, C]
five = 	[C, C, C,
		C, X, X,
		C, C, C,
		X, X, C,
		C, C, C]
six = 	[C, C, C,
		C, X, X,
		C, C, C,
		C, X, C,
		C, C, C]
seven =	[C, C, C,
		X, X, C,
		X, X, C,
		X, X, C,
		X, X, C]
eight =	[C, C, C,
		C, X, C,
		C, C, C,
		C, X, C,
		C, C, C]
nine = 	[C, C, C,
		C, X, C,
		C, C, C,
		X, X, C,
		C, C, C]

link = {'0':zero, '1':one,'2':two,'3':three,'4':four,'5':five,'6':six,'7':seven,'8':eight,'9':nine}

sense = SenseHat()

sense.clear()

def set_number(number,x_offset,y_offset):
	matrix = link[str(number)] # gives the matrix representing the number
	x = 0
	y = 0
	nb = 0
	for el in matrix:
		if nb % 3 == 0:
			y+=1
			x=0
		if el == sense.get_pixel(x+x_offset,y+y_offset): # skip pixels that are already displayed
			pass
		elif el != None: # set pixel
			sense.set_pixel(x+x_offset,y+y_offset,C[0],C[1],C[2])
		else: # unset pixel
			sense.set_pixel(x+x_offset,y+y_offset,0,0,0)
		x+=1
		nb+=1

def display_number(number):
	if number > 0 and number < 100:
		d = number % 10
		set_number(d,5,1)
		u = floor(number/10)
		set_number(u,1,1)

display_number(2)
