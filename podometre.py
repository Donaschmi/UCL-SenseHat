from sense_hat import SenseHat,ACTION_RELEASED
from time import sleep,time
from math import pow,sqrt

# Setup
sense = SenseHat()
sense.low_light = True


# Fonction qui renvoie le temps en ms
current_milli_time = lambda: int(round(time() * 1000))

start_time = current_milli_time()

# Variables
R = [255, 0, 0]
G = [127, 255, 0]
mean = 0.0
step_count = 0

# display red screen to show inactivity
display = [R] * 64
sense.set_pixels(display)

# Wait for an event in order to begin
print("Appuyer sur le joystick pour commencer")
event = sense.stick.wait_for_event()
while event.action != ACTION_RELEASED:
	event = sense.stick.wait_for_event()


# display red screen to show start of logging
display = [G] * 64
sense.set_pixels(display)
start_time = current_milli_time()

# infinite loop
# TODO: stop loop on joystick press?
while True:

	## TODO: log all data? => RAM/DISK?
	## TODO: 
	##
	t = current_milli_time()
	acc = sense.get_accelerometer_raw()
	x = acc['x']
	y = acc['y']
	z = acc['z']
	print("x:%s, y:%s, z:%s"%(x,y,z))
	mag = sqrt(pow(x,2)+pow(y,2)+pow(z,2))
	print(mag)
	
	# TODO: substract mean from mag to remove constant effects like gravity...
	# for mean we need to have stored previous data...
	
	# Determine the threshold value to increase step_count
	if (mag > 1.0):
		step_count += 1
	sleep(0.2)
	
	# stop after 5 seconds
	if (t-start_time > 5000):
		break


# Clean before exit
sense.clear()
print(str(step_count))



"""

"""




	
