from pandac.PandaModules import NodePath
from pandac.PandaModules import CardMaker

import resource

CREATURE_WIDTH = 3
CREATURE_HEIGHT = 6
CARD_MAKER = CardMaker('creature_generator')
CARD_MAKER.setFrame(0, CREATURE_WIDTH, 0, CREATURE_HEIGHT)

class Creature(object):
    def __init__(self):
        self.nodepath = NodePath(repr(self))
        node = self.nodepath.attachNewNode(CARD_MAKER.generate())
        node.setTexture(self.texture)
        node.setTwoSided(True)
        node.setTransparency(True)
        self.nodepath.setBillboardPointEye()

class Robot(Creature):
    texture = resource.TEXTURES.asterisk_orange

class Human(Creature):
    texture = resource.TEXTURES.user
