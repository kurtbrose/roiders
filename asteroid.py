'''
This module contains functions for handling an abstract asteroid.

Testing has determined the graphics card is the performance bottleneck.
Python classes Asteroid, Level, TileGroup are designed for ease of use.
Performance is not a concern here.

The main interface is the Asteroid class.
'''
import random
import math

from pandac.PandaModules import PandaNode
from pandac.PandaModules import NodePath
from pandac.PandaModules import CardMaker

import resource

LEVEL_SPACING = 25
TILE_SIZE  = 10
TILE_GRP_SIZE = 5 #length and width of each tile group (grouped for performance)

CARD_MAKER = CardMaker('tile_generator')
CARD_MAKER.setFrame(0, TILE_SIZE, 0, TILE_SIZE)

#need to figure out how to do pathfinding -- what kind of data structures required here?

class TileType(object):
	texture = None

class Empty(TileType):
	def __init__(self):
		self.passable = True

class Natural(TileType):
	def __init__(self):
		self.passable = False

	def tunnel(self, direction):
		self.passable = True # TODO: figure out how to draw the tunnel

class Rock(Natural):
	texture = resource.TEXTURES.rocks


class Asteroid(object):
	def __init__(self, name="Asteroid"):
		self.name = name
		self.nodepath = NodePath(PandaNode("Asteroid"+name))
		self.contents = {}
		self.levels = {}

	@classmethod
	def make_spheroid(cls, tile_type, radius=30, name="Asteroid"):
		self = cls(name)
		z_scale = 4
		z_len = int(radius/z_scale)
		for z in range(-z_len, z_len):
			for x in range(-radius, radius):
				for y in range(-radius, radius):
					dist = ((z*z_scale)**2+x**2+y**2)**0.5
					if dist < radius:
						self.update(x,y,z, tile_type())
					elif dist < radius + 3:
						self.update(x,y,z, Empty())
		self.redraw()
		return self

	def update(self, x, y, level, tile_type):
		pos = (x,y,level)
		self.contents[pos] = tile_type
		if level not in self.levels:
			self.levels[level] = Level(self, level)
			self.levels[level].nodepath.setPos(0, level*LEVEL_SPACING, 0)
		self.levels[level].update(x, y, tile_type.texture)

	def redraw(self):
		for level in self.levels.values():
			level.redraw()

	def get_pos(self, x, y, level):
		'convert asteroid coordinates to position'
		pos_x, pos_y, pos_z = self.nodepath.getPos()
		return (pos_x + TILE_SIZE*(x+0.5), 
			    pos_y + level * LEVEL_SPACING, 
			    pos_z + TILE_SIZE*(y+0.5))

	def get(self, x, y, level):
		return self.contents.get((x,y,level))

	def get_collision_pos(self, collision):
		point3 = collision.getSurfacePoint(self.nodepath)
		x = int(math.floor(point3.getX()/TILE_SIZE))
		y = int(math.floor(point3.getZ()/TILE_SIZE))
		z = int(round(point3.getY()/LEVEL_SPACING))
		return x,y,z


class Level(object):
	'''
	Represents one level of the asteroid.
	Internal to Asteroid mostly.
	'''
	def __init__(self, parent, num):
		self.parent = parent
		self.name = "{0}-Level#{1}".format(parent.name, num)
		#create one root nodepath for the overall level
		self.nodepath = NodePath(PandaNode(self.name))
		self.tile_groups = {}
		self.nodepath.reparentTo(self.parent.nodepath)
		
	def update(self, x, y, texture):
		tgs = TILE_GRP_SIZE
		tg_pos = tg_x, tg_y = x/tgs, y/tgs
		if tg_pos not in self.tile_groups:
			self.tile_groups[tg_pos] = TileGroup(self, tg_x, tg_y)
			scale = TILE_GRP_SIZE * TILE_SIZE
			self.tile_groups[tg_pos].nodepath.setPos(tg_x*scale, 0, tg_y*scale)
		self.tile_groups[tg_pos].update(x%tgs, y%tgs, texture)

	def redraw(self):
		for tg in self.tile_groups.values():
			tg.redraw()
		

class TileGroup(object):
	'group and flatten tiles, for rendering performance'
	def __init__(self, parent, tile_x, tile_y):
		self.parent = parent
		self.name = "{0}:TileGroup({1},{2})".format(parent.name,tile_x, tile_y)
		self.nodepath = NodePath(PandaNode(self.name))
		self.textures = [[None]*TILE_GRP_SIZE for i in range(TILE_GRP_SIZE)]
		self.nodepath.reparentTo(self.parent.nodepath)
		self.dirty = False

	def update(self, x, y, texture):
		if self.textures[x][y] != texture:
			self.textures[x][y] = texture
			self.dirty = True

	def redraw(self):
		if not self.dirty:
			return #nothing has changed, no need to redraw
		container = NodePath(PandaNode(self.name+"container"))
		for i in range(TILE_GRP_SIZE):
			for j in range(TILE_GRP_SIZE):
				cur = self.textures[i][j]
				if cur:
					node = container.attachNewNode(CARD_MAKER.generate())
					node.setTexture(cur)
					node.setTwoSided(True)
					node.setPos(i*TILE_SIZE, 0, j*TILE_SIZE)
		container.flattenStrong()
		for child in self.nodepath.getChildren():
			child.removeNode()
		container.reparentTo(self.nodepath)
		self.dirty = False


def tunnel(asteroid):
	'cut out pieces of the asteroid; allow for pathing tests'
	#dig the initial tunnel through center of mass
	for z in range(-50, 50):
		asteroid.update(0, 0, z, Empty())
	for i in range(70):
		#make a bunch of random cuts that intersect the tunnel
		ys = range(0, 100)
		xs = [0]*len(ys)
		if random.random() > 0.5:
			ys = [-1*e for e in ys]
		if random.random() > 0.5:
			xs, ys = ys, xs
		zs = [random.randint(-50, 50)]*len(ys)
		for x, y, z in zip(xs, ys, zs):
			if asteroid.get(x,y,z):
				asteroid.update(x,y,z,Empty())
	asteroid.redraw()

