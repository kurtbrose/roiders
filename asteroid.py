'''
This module contains functions for handling an abstract asteroid.

'''
import array

from pandac.PandaModules import PandaNode
from pandac.PandaModules import NodePath
from pandac.PandaModules import CardMaker


def generate_contents(x, y, z):
    pass

class Asteroid(object):
    def __init__(self, x, y, z, contents=None):
        pass
    

LEVEL_SIZE = 1000 #length and width of each asteroid level, in tiles
TILE_SIZE  = 10

#need to figure out how to do pathfinding -- what kind of data structures required here?

class TileType(object):
	def __init__(self, texture):
		self.texture = texture

class ObjectType(object):
	pass

class Creature(object):
	pass

class Robot(Creature):
	pass

class Human(Creature):
	pass

class Level(object):
	'''
	Represents one level of the asteroid.
	'''
	def __init__(self, num, contents=None):
		self.contents = array.array('L')
		self.nodepath = NodePath(PandaNode("level"+str(num)))

	def update(self, x, y, tiletype):
		self.contents[x][y] = tiletype
		self.nodepath.


def init_textures(app):
	TEXTURES['blank'] = app.loader.loadTexture('icons/arrow_out.png')
	TILE_TYPES['empty'] = TEXTURES['blank']

TEXTURES = {}

TILE_TYPES = {}