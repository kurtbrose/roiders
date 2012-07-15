'''
This module contains functions for handling an abstract asteroid.

'''
import array


def generate_contents(x, y, z):
    pass

class Asteroid(object):
    def __init__(self, x, y, z, contents=None):
        pass
    

LEVEL_SIZE = 1000 #length and width of each asteroid level

#need to figure out how to do pathfinding -- what kind of data structures required here?

class Level(object):
	'''
	Represents one level of the asteroid.
	'''
	def __init__(self, contents=None):
		self.contents = array.array('L')

