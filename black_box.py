#!/usr/bin/python

"""black_box.py: """

__author__ = "Donatien Schmitz"
__copyright__ = "Copyright 2018, Donatien Schmitz"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "schmitzd@oasis.uclouvain.be"
__status__ = "Production"

import sys
import time
import signal
from sense_hat import SenseHat, ACTION_RELEASED


class BlackBox:

    def __init__(self, destRoll, destPitch):

        # Initialize and clear the SenseHat
        self.sense = SenseHat()
        self.sense.clear()


        self.initial_pos = self.sense.get_orientation()
        self.initial_roll =  self.initial_pitch = 0
        self.destination = {'roll': destRoll, 'pitch': destPitch}

        self.prevY = self.prevX = 0

        self.speed = 0


        for i in range(0, 8): # Set the pixels for the speed
            self.sense.set_pixel(7, i, 80, 0, 0)

    def launch(self):
        """
        TODO
        """

        while True:
            curr_pos = self.sense.get_orientation()

            delta_roll = curr_pos["roll"] - self.initial_pos["roll"]
            delta_roll = (delta_roll + 180) % 360 - 180 # We want a value between 180 and ~180

            delta_pitch = curr_pos["pitch"] - self.initial_pos["pitch"]
            delta_pitch = (delta_pitch + 180) % 360 - 180

            # Indicate which pixel will be lighten
            x = 0
            y = 0

            # Indicate if the roll/pitch direction is correct
            prev_roll = False
            prev_pitch = False

            # We can manipulate the delta however we liken we picked a 1/10 ratio
            self.initial_roll += (delta_roll / 10.0) * (self.speed / 100.0)
            self.initial_pitch += (delta_pitch / 10.0) * (self.speed / 100.0)

            remain_roll = (self.destination['roll'] - self.initial_roll + 180) % 360 - 180
            remain_pitch = (self.destination['pitch'] - self.initial_pitch + 180) % 360 - 180

            # Check if we are in the right direction and if not, indicate if to the
            # left or right  and in what mesure
            if remain_roll < 0:
                if remain_roll > -20: # We are in the right direction
                    y = 4
                    prev_roll = True
                elif remain_roll > -50:
                    y = 5
                elif remain_roll > -100:
                    y = 6
                else:
                    y = 7
            else:
                if remain_roll > 100:
                    y = 1
                elif remain_roll > 50:
                    y = 2
                elif remain_roll > 20:
                    y = 3
                else:
                    y = 4
                    prev_roll = True

            if remain_pitch < 0:
                if remain_pitch > -20:
                    x = 3
                    prev_pitch = True
                elif remain_pitch > -50:
                    x = 4
                elif remain_pitch > -100:
                    x = 5
                else:
                    x = 6
            else:
                if remain_pitch > 100:
                    x = 0
                elif remain_pitch > 50:
                    x = 1
                elif remain_pitch > 20:
                    x = 2
                else:
                    prev_pitch = True
                    x = 3

            self.sense.set_pixel(self.prevX, self.prevY, 0, 0, 0)

            pixel_speed = min(8, self.speed / 10.0)

            # Update the speed-o-meter
            for i in range(0, 8):
                if i >= 8 - pixel_speed:
                    self.sense.set_pixel(7, i, 0, 60, 0)
                else:
                    self.sense.set_pixel(7, i, 60, 0, 0)

            if prev_roll and prev_pitch:
                self.sense.set_pixel(3, 4, 0, 255, 0)
            else:
                self.sense.set_pixel(3, 4, 255, 0, 255)
                self.sense.set_pixel(x, y, 255, 0, 0)

            self.prevX = x
            self.prevY = y

            time.sleep(0.5)

    def upPressed(self, event):
        """
        TODO
        """
        if event.action != ACTION_RELEASED:
            self.speed = min(self.speed + 1, 101)

    def downPressed(self, event):
        """
        TODO
        """
        if event.action != ACTION_RELEASED:
            self.speed = max(self.speed - 1, 0)

    def mount(self):
        """
        TODO
        """
        self.sense.stick.direction_up = self.upPressed
        self.sense.stick.direction_down = self.downPressed

if __name__ == '__main__':
    black_box = BlackBox(0, 0)
    black_box.mount()
    black_box.launch()
