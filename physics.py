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
    zero_plane = [[0,0,0]]*3
    hot_plane  = [[0,0,0],[0,100,0],[0,0,0]]
    values = [zero_plane, hot_plane, zero_plane]
    resistances = [[[10]*3]*3]*3
    capacities  = [[[10]*3]*3]*3
    s = Simulation(values, resistances, capacities)
    for i in range(10):
        print s.values
        s.step()
