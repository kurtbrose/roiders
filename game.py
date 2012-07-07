from direct.showbase import ShowBase
from direct.task import Task

from pandac import PandaModules as pm
from pandac.PandaModules import OrthographicLens
from pandac.PandaModules import LineSegs
from pandac.PandaModules import PandaNode
from pandac.PandaModules import NodePath


def make_grid(name, rows, cols, size, thickness):
    lines = LineSegs()
    lines.setColor(pm.VBase4(0,0,0,1))
    lines.setThickness(thickness)
    #compute some constants
    x_size = cols*size
    y_size = rows*size
    bottom = -y_size/2
    top    =  y_size/2
    left   = -x_size/2
    right  =  x_size/2
    #draw vertical lines
    for i in range(0, cols):
        x_pos = i*size - left
        lines.moveTo(x_pos, bottom, 0)
        lines.drawTo(x_pos, top, 0   )
    #draw horizontal lines
    for i in range(0, rows):
        y_pos = i*size - bottom
        lines.moveTo(left,  y_pos, 0)
        lines.drawTo(right, y_pos, 0)
    #set up nodes and paths
    node       = PandaNode(name)
    nodepath   = NodePath(node)
    lines_node = lines.create()
    lines_node_path = NodePath(lines_node)
    lines_node_path.setAntialias(pm.AntialiasAttrib.MLine)
    lines_node_path.reparentTo(nodepath)
    return nodepath

class MyApp(ShowBase.ShowBase):
    def __init__(self):
        ShowBase.ShowBase.__init__(self)
        '''
        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)
        '''
        self.grid = make_grid("grid", 10, 10, 20, 10)
        self.grid.setPos(0, 0, 0)
        self.grid.reparentTo(self.render)
        
        for i in range(10):
            g = make_grid("grid"+str(i), 100, 100, 5, 1)
            g.reparentTo(self.render)
            g.setPos(10*i, 10*i, 10*i)
        
        lens = OrthographicLens()
        lens.setFilmSize(20, 15)
        self.cam.node().setLens(lens)
        
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
    
    def spinCameraTask(self, task):
        from math import pi, sin, cos
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        #self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        #self.camera.setHpr(angleDegrees, 0, 0)
        
        p = (task.time * 1.0) % 100
        self.grid.setPos(p, p, p)
        return Task.cont

app = MyApp()
app.run()

