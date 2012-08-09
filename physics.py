'''
This module implements quick & dirty physics simulation that is feasible
to do as the game runs.

The method is a limited Finite Difference.
At each time step, heat/pressure flows between adjacent nodes.

Empirical testing of number of simulations and step size:
(for a 50x50x50 simulation area)
1, 19ms
2, 32ms
3, 57ms

Experiments with thread showed no performance benefite.
(Maybe numpy already multi-threads basic array operations?)
'''
import numpy

class Simulation(object):
    def __init__(self, values, resistances, capacities):
        '''
        All parameters are list of lists of lists;
        they should be rectangular

        values -- initial values
        resistances -- inverse to flow rate; e.g. heat resistance, air friction
        capacity -- amount stored per value; e.g. heat capacity, volume

        The edges of the simulation region are considered to be a 0-value sink
        of infinite capacity
        '''
        self.values      = numpy.array(values,      dtype=numpy.float64)
        self.resistances = numpy.array(resistances, dtype=numpy.float64)
        self.capacities  = numpy.array(capacities,  dtype=numpy.float64)
        #compute resistance in each direction for each point of flow
        self.res_x = (self.resistances[:-1,:,:] + self.resistances[1:,:,:])/2
        self.res_y = (self.resistances[:,:-1,:] + self.resistances[:,1:,:])/2
        self.res_z = (self.resistances[:,:,:-1] + self.resistances[:,:,1:])/2

        self.thread = None

    def step(self):
        #TODO: can the number of matrix operations be reduced?
        diff_x = self.values[1:,:,:] - self.values[:-1,:,:]
        diff_y = self.values[:,1:,:] - self.values[:,:-1,:]
        diff_z = self.values[:,:,1:] - self.values[:,:,:-1]

        left_right_flow = diff_x / self.res_x
        up_down_flow    = diff_y / self.res_y
        in_out_flow     = diff_z / self.res_z

        self.values[:-1,  :,  :] += left_right_flow / self.capacities[:-1,  :,  :]
        self.values[ 1:,  :,  :] -= left_right_flow / self.capacities[1: ,  :,  :]
        self.values[  :,:-1,  :] += up_down_flow    / self.capacities[  :,:-1,  :]
        self.values[  :, 1:,  :] -= up_down_flow    / self.capacities[  :, 1:,  :]
        self.values[  :,  :,:-1] += in_out_flow     / self.capacities[  :,  :,:-1]
        self.values[  :,  :, 1:] -= in_out_flow     / self.capacities[  :,  :, 1:]



def test():
    import copy
    zero_plane = [[0]*50]*50
    hot_plane  = copy.deepcopy(zero_plane)
    hot_plane[25][25] = 100
    values = [zero_plane] * 50
    values[25] = hot_plane
    resistances = [[[10]*50]*50]*50
    capacities  = [[[10]*50]*50]*50
    s = Simulation(values, resistances, capacities)
    s2 = Simulation(values, resistances, capacities)
    s3 = Simulation(values, resistances, capacities)
    import time
    for i in range(200):
        a = time.time()
        s.step()
        s2.step()
        s3.step()
        print time.time() - a
