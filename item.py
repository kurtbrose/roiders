'''
Items -- there are inanimate objects which can be carried around.
'''
class Item(object):
    def __init__(self):
        pass

class Material(Item):
    #used to build stuff; e.g. "metal bar"
    pass

class Component(Material):
    #used to build stuff, but more complex; e.g. camera, motor, CPU
    pass

class Tool(Item):
    #used to do tasks, but not used up; e.g. eletrical welder
    pass

class Equipment(Item):
    #can be worn or equipped to enable actions; e.g. space suit
    pass 



class SmallMotor(Item):
    mass = 3

#used to generate gravity-like force; needed for many purposes:
#plant growth, eliminating air bubbles from liquids
class Centrifuge(Item):
    pass