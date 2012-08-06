'''
Buildings are immobile, and must be dissassembeld and moved as parts.
Some buildings require vacuum, some require atmosphere.
'''
class Building(object):
    '''
    An immobile construction taking up one or more tiles.
    '''
    pass

class Workshop(Building):
    '''
    A building used to turn one item into another.
    '''
    pass

class Reactor(Building):
    '''
    Sources and/or sinks, more continuous process.
    e.g. power plant, CO2 scrubber, Oxygen Source
    '''
    pass

class Lab(Workshop):
    '''
    Used to analyze or perform very fine work.
    (materials are not consumed or generated)
    '''
    pass

class Biotope(Workshop):
    '''
    A workshop whose purpose is maintaining living creatures.
    e.g. hyroponic growth lab 
    '''
    pass
