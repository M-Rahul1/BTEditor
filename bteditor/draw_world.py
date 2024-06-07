#!/usr/bin/env python3
"""
Class to print the state of the coffee-serving scenario
"""

import math
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from matplotlib.patches import RegularPolygon, Rectangle

class Object:
    """ Class for graphical objects parameters """
    def __init__(self, x, y, l, h, line='black', fill='white'):
        """
        Initialize the object with origin, dimension and graphical properties.
        """
        self.origin = (x, y)
        self.length = l
        self.height = h
        self.line = line
        self.fill = fill

    def set_origin(self, x, y):
        """
        Function to set the pose of an object.
        """
        self.origin = (x, y)

class CoffeeWorldUI:
    """ User Interface that allows prints the coffee-serving world state """

    def __init__(self):
        """
        Initialize the static objects in the coffee-serving world.
        """
        # initialize Map object
        self.map = Object(x=0, y=0, l=25, h=15, line='black', fill='white')
        self.emptycup = Object(x=10, y=8, l=5, h=5, line='black', fill='white')
        self.sugarcup = Object(x=5, y=2, l=1, h=1, line='black', fill='grey')
        self.milkcup = Object(x=10, y=2, l=1, h=1, line='black', fill='darkgrey')
        self.coffeecup = Object(x=15, y=2, l=1, h=1, line='black', fill='brown')

    def get_figure(self):
        """
        Return the figure object
        """
        return self.figure, self.axes

    def reset_world(self):
        """
        Reset the world with static objects and robot in home position.
        """
        self.figure, self.axes = plt.subplots()

        # add the Map
        self.axes.add_patch(Rectangle(self.map.origin, self.map.length, self.map.height, \
                                      edgecolor=self.map.line, facecolor=self.map.fill))

        # add the Empty Cup
        self.axes.add_patch(Rectangle(self.emptycup.origin, self.emptycup.length, self.emptycup.height, \
                                      edgecolor=self.emptycup.line, facecolor=self.emptycup.fill))
        self.axes.text(self.emptycup.origin[0] + 0.5, self.emptycup.origin[1] - 0.5, 'Empty Cup')

        # add the Sugar Cup
        self.axes.add_patch(Rectangle(self.sugarcup.origin, self.sugarcup.length, self.sugarcup.height, \
                                      edgecolor=self.sugarcup.line, facecolor=self.sugarcup.fill))
        self.axes.text(self.sugarcup.origin[0] + 0.5, self.sugarcup.origin[1] - 0.5, 'Sugar Cup')

        # add the Milk Cup
        self.axes.add_patch(Rectangle(self.milkcup.origin, self.milkcup.length, self.milkcup.height, \
                                      edgecolor=self.milkcup.line, facecolor=self.milkcup.fill))
        self.axes.text(self.milkcup.origin[0] + 0.5, self.milkcup.origin[1] - 0.5, 'Milk Cup')

        # add the Coffee Cup
        self.axes.add_patch(Rectangle(self.coffeecup.origin, self.coffeecup.length, self.coffeecup.height, \
                                      edgecolor=self.coffeecup.line, facecolor=self.coffeecup.fill))
        self.axes.text(self.coffeecup.origin[0] + 0.5, self.coffeecup.origin[1] - 0.5, 'Coffee Cup')

    def add_robot(self, pose):
        """
        Add the robot in the UI.
        """
        self.axes.add_patch(RegularPolygon(pose, 8, radius=1, orientation=math.pi / 8, edgecolor='black', facecolor='paleturquoise'))
        self.axes.text(pose[0] - 0.4, pose[1] - 0.2, 'R', fontweight='bold')

    def add_items(self, item_name, quantity):
        """
        Add specified items to the appropriate cup.
        """
        if item_name == 'sugar':
            self.add_sugar(quantity)

    def add_sugar(self, quantity):
        """
        Add sugar to the empty cup.
        """
        self.reset_world()
        self.sugarcup.set_origin(self.emptycup.origin[0] + 1, self.emptycup.origin[1] + 1)
        self.axes.add_patch(Rectangle(self.sugarcup.origin, self.sugarcup.length, self.sugarcup.height, \
                                      edgecolor=self.sugarcup.line, facecolor=self.sugarcup.fill))
        self.axes.text(self.sugarcup.origin[0] + 0.5, self.sugarcup.origin[1] - 0.5, 'Sugar')

    def add_milk(self, quantity):
        """
        Add milk to the empty cup.
        """
        self.reset_world()
        for i in range(quantity):
            self.milkcup.set_origin(self.emptycup.origin[0] + 1 + i, self.emptycup.origin[1] + 2)
            self.axes.add_patch(Rectangle(self.milkcup.origin, self.milkcup.length, self.milkcup.height, \
                                          edgecolor=self.milkcup.line, facecolor=self.milkcup.fill))
            self.axes.text(self.milkcup.origin[0] + 0.5, self.milkcup.origin[1] - 0.5, 'Milk')

    def add_coffee(self, quantity):
        """
        Add coffee to the empty cup.
        """
        self.reset_world()
        for i in range(quantity):
            self.coffeecup.set_origin(self.emptycup.origin[0] + 1 + i, self.emptycup.origin[1] + 3)
            self.axes.add_patch(Rectangle(self.coffeecup.origin, self.coffeecup.length, self.coffeecup.height, \
                                          edgecolor=self.coffeecup.line, facecolor=self.coffeecup.fill))
            self.axes.text(self.coffeecup.origin[0] + 0.5, self.coffeecup.origin[1] - 0.5, 'Coffee')

    def add_state(self, world_state):
        """
        Add the world state in the UI.
        """
        self.add_robot(world_state.robot)
        # Assumes world_state has fields: robot, items
        for item, quantity in world_state.items.items():
            self.add_items(item, quantity)

    def print_world(self, name):
        """
        Print the world with added patches.
        """
        self.axes.plot()
        path = './tests/' + name + '.svg'
        self.figure.savefig(path)
        plt.close(self.figure)
