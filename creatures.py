from pandac.PandaModules import NodePath
from pandac.PandaModules import CardMaker

CREATURE_WIDTH = 3
CREATURE_HEIGHT = 6
CARD_MAKER = CardMaker(0, CREATURE_WIDTH, 0, CREATURE_HEIGHT)

class Creature(object):
    def __init__(self):
        self.nodepath = NodePath()
        node = self.nodepath.attachNewNode(CARD_MAKER.generate())
        node.setTexture(self.texture)
        node.setTwoSided(True)
        self.nodepath.setBillboardPointEye()

class Robot(Creature):
    texture = None

class Human(Creature):
    texture = None
