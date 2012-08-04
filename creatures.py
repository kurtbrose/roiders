import heapq

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
    #heuristic function -- manhattan distance
    def H(pos):
        dist = abs(pos[0]-dest[0])+abs(pos[1]-dest[1])+abs(pos[2]-dest[2])
        fuzz = (pos[0] ^ pos[1] ^ pos[2]) * 1e-7
        return dist + fuzz

    G = {src:0} #lowest weight to reach a given node
    F_heap = [(H(src), src)]
    parents = {} #best parent for a given node
    open_set = set([src])
    closed_set = set()

    def follow_path(pos):
        path = []
        while pos in parents:
            path.append(pos)
            pos = parents[pos]
        path.append(pos)
        return path #return path in "backwards" order so positions can be popped

    while F_heap:
        x,y,z = pos = heapq.heappop(F_heap)[1]
        if pos in closed_set:
            continue #skip, this was a more expensive route
        if pos == dest:
            return follow_path(pos)
        open_set.remove(pos)
        closed_set.add(pos)
        for x2, y2, z2 in [(x+1, y, z), (x-1, y, z), (x, y+1, z),
                            (x, y-1, z), (x, y, z+1), (x, y, z-1)]:
            pos2 = x2,y2,z2
            if pos2 in closed_set:
                continue
            tile = asteroid.get(x2, y2, z2)
            if tile and tile.passable:
                open_set.add(pos2)
                if pos2 not in G or G[pos2] > G[pos] + 1:
                    parents[pos2] = pos
                    G[pos2] = G[pos] + 1
                    heapq.heappush(F_heap, (H(pos2) + G[pos2], pos2))
            else:
                closed_set.add(pos2)
    #couldn't find a path
    return None



