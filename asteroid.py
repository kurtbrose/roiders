'''
This module contains functions for handling an abstract asteroid.
An asteroid is represented internally as dimensions, plus a string of contents.

Contents code:
AA-MMMMMM

AA = 00, vacuum
AA = 01, unbreathable air: low pressure
AA = 10, unbreathable air: high C02
AA = 11, breathable air

'''


def generate_contents(x, y, z):
    pass

class Asteroid(object):
    def __init__(self, x, y, z, contents=None):
        pass
    
    