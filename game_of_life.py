#!/usr/bin/env python

"""game_of_life.py: """

__author__ = "Donatien Schmitz"
__copyright__ = "Copyright 2018, Donatien Schmitz"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "donatien.schmitz@student.uclouvain.be"
__status__ = "Production"

from sense_hat import SenseHat, ACTION_RELEASED, ACTION_HELD, ACTION_PRESSED
from signal import pause
import copy
import numpy as np

class GameOfLife:
    def __init__(self, N=8):
        self.red = [255, 0, 0]
        self.green = [0, 255, 0]
        self.C = [0, 0, 255]
        self.O = [0, 0, 0]

        self.sense = SenseHat()

        self.playing = False
        self.N = N
        self.matrix = [self.O] * 64
        self.old_grid = np.zeros(N*N)
        self.new_grid = np.zeros(N*N)
        self.currX = 3
        self.currY = 3

    def draw(self):
        """
        Convert the numpy array into a 64 matrix with colors then displays it on the monitor.

        Parameters
        ----------
        /

        Returns
        -------
        /

        """
        for i in range(self.N):
            for j in range(self.N):
                if self.old_grid[j*8 + i] == 1:
                    self.matrix[j*8 + i] = self.C
                else:
                    self.matrix[j*8 + i] = self.O
        self.sense.set_pixels(self.matrix)

    def neighbours(self, x, y):
        """
        Return the number of living cells adjacent to the cell in pos (x,y).

        Parameters
        ----------
        x: int
            X-axis position
        y: int
            Y-axis position

        Returns
        -------
        count: int
            Number of living cells adjacent
        """
        count = 0
        for i in range(3):
            for j in range(3):
                new_x = (x+i+7)%8
                new_y = (y+j+7)%8
                if self.old_grid[new_y * 8 + new_x] == 1:
                    count += 1

        if self.old_grid[y * 8 + x] == 1:
            count-=1

        return count

    def next_gen(self):
        """
        Compute the next generation of living cells and update the matrix.

        For each index of the matrix, get the number of living neighbour cells
        and check if there should be a cell in the index or not according to
        the rules of Conway's Game of Life.
        Finally copy the new matrix into the old one.

        Parameters
        ----------
        /

        Returns
        -------
        /
        """
        for i in range(self.N):
            for j in range(self.N):
                index = j*8+i
                neighs = self.neighbours(i, j)
                curr_state = self.old_grid[index]
                if (curr_state == 1 and neighs < 2):
                    self.new_grid[index] = 0
                elif(curr_state == 1 and (neighs == 2 or neighs == 3)):
                    self.new_grid[index] = 1
                elif(curr_state == 1 and neighs > 3):
                    self.new_grid[index] = 0
                elif(curr_state == 0 and neighs == 3):
                    self.new_grid[index] = 1
                else:
                    self.new_grid[index] = 0

        if np.array_equal(self.old_grid, self.new_grid):
            self.C = self.red
        self.old_grid = self.new_grid.copy()

    def foo(self):
        """
        Used to dismount the stick.

        Parameters
        ----------
        /

        Returns
        -------
        """
        return

    def dismount(self):
        """
        Dismount the stick directions so it doesn't interfere.

        Parameters
        ----------
        /

        Returns
        -------
        /
        """
        self.sense.stick.direction_up = self.foo
        self.sense.stick.direction_down = self.foo
        self.sense.stick.direction_right = self.foo
        self.sense.stick.direction_left = self.foo

    def pushed_up(self, event):
        """
        Upon getting pressed, move the current cell 1 pixel up

        Parameters
        ----------
        event: Event
            Either ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

        Returns
        -------
        /
        """
        if event.action != ACTION_RELEASED:
            self.currY = (self.currY - 1) % 8

    def pushed_down(self, event):
        """
        Upon getting pressed, move the current cell 1 pixel down

        Parameters
        ----------
        event: Event
            Either ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

        Returns
        -------
        /
        """
        if event.action != ACTION_RELEASED:
            self.currY = (self.currY + 1) % 8

    def pushed_right(self, event):
        """
        Upon getting pressed, move the current cell 1 pixel right

        Parameters
        ----------
        event: Event
            Either ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

        Returns
        -------
        /
        """
        if event.action != ACTION_RELEASED:
            self.currX = (self.currX + 1) % 8

    def pushed_left(self, event):
        """
        Upon getting pressed, move the current cell 1 pixel left

        Parameters
        ----------
        event: Event
            Either ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

        Returns
        -------
        /
        """
        if event.action != ACTION_RELEASED:
            self.currX = (self.currX - 1) % 8

    def pushed_middle(self, event):
        """
        Perform several actions depending on the game playing state and the event

        If the state is playing, pressing or holding the middle button will display the next generation
        If the state is not playing, pressing the button will change the state of the current cell.
        If the state is not playing, holding the button will change the playing state and launch the first generation
        Parameters
        ----------
        event: Event
            Either ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

        Returns
        -------
        /
        """
        if not self.playing:
            if event.action != ACTION_RELEASED:
                self.old_grid[self.currY*8+self.currX] = 1 if self.old_grid[self.currY * 8 + self.currX] == 0 else 0
            if event.action == ACTION_HELD:
                self.playing = True
                self.dismount()
                self.next_gen()
        else:
            if (event.action == ACTION_PRESSED or event.action == ACTION_HELD):
                self.next_gen()

    def refresh(self):
        """
        Clear the monitor and draw the current matrix.

        Parameters
        ----------
        /

        Returns
        -------
        /
        """
        self.sense.clear()
        self.draw()
        if not self.playing:
            is_cell = self.green if self.old_grid[self.currY*8 + self.currX] == 1 else self.red
            self.sense.set_pixel(self.currX, self.currY, is_cell)

    def mount(self):
        """
        Bind each stick direction to its corresponding function

        Parameters
        ----------
        /

        Returns
        -------
        /
        """
        self.sense.stick.direction_up = self.pushed_up
        self.sense.stick.direction_down = self.pushed_down
        self.sense.stick.direction_right = self.pushed_right
        self.sense.stick.direction_left = self.pushed_left
        self.sense.stick.direction_middle = self.pushed_middle
        self.sense.stick.direction_any = self.refresh


if __name__ == "__main__":
    game = GameOfLife()
    game.mount()
    game.refresh()
    pause()
