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
        self.pos = None
        self.cur_path = []

    def goto(self, pos, asteroid):
        self.cur_path = find_path(self.pos, pos, asteroid)

class Robot(Creature):
    texture = resource.TEXTURES.asterisk_orange

class Human(Creature):
    texture = resource.TEXTURES.user

    def __init__(self):
        super(Human, self).__init__()


class JobQueue(object):
    pass


def find_path(src, dest, asteroid):
    'find a path from source to destination'
    parents = {}
    todo = set([src])
    iteration = 0
    while todo:
        iteration += 1
        if iteration % 100000 == 0:
            print "iteration", iteration, "todo_len", len(todo) 
        x, y, z = curpos = todo.pop()
        #if we have reached the destination, trace the found path
        if curpos == dest:
            path = []
            while curpos != src:
                path.append(curpos)
                curpos = parents[curpos]
            return path #path in "backwards" order so items can be popped
        #otherwise, add the current steps to the path
        for x2, y2, z2 in [(x+1, y, z), (x-1, y, z), (x, y+1, z),
                            (x, y-1, z), (x, y, z+1), (x, y, z-1)]:
            if (x2, y2, z2) in parents:
                continue #already seen
            tile = asteroid.get(x2, y2, z2)
            if tile and tile.passable:
                parents[(x2, y2, z2)] = curpos
                todo.add((x2, y2, z2))
    print "giving up, checked positions ", len(parents)
    #couldn't find a path, return None
    return None


