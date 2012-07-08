import os, os.path

from panda3d.core import Filename
from panda3d import core

from direct.showbase import ShowBase
from direct.showbase import Loader
from direct.task import Task

from pandac import PandaModules as PM
from pandac.PandaModules import OrthographicLens
from pandac.PandaModules import LineSegs
from pandac.PandaModules import PandaNode
from pandac.PandaModules import NodePath

#set up some loading constants
DIR = str(Filename.fromOsSpecific(os.path.dirname(os.path.abspath(__file__))))
#convert back to base string from panda type
ASSET_DIR = DIR+"/assets/"
PM.getModelPath().appendPath(ASSET_DIR) 

def make_grid(name, rows, cols, size, thickness):
    lines = LineSegs()
    lines.setColor(PM.VBase4(0,0,0,1))
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
        lines.drawTo(x_pos, top, 0)
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
    lines_node_path.setAntialias(PM.AntialiasAttrib.MLine)
    lines_node_path.reparentTo(nodepath)
    return nodepath

class MyApp(ShowBase.ShowBase):
    def __init__(self):
        ShowBase.ShowBase.__init__(self)
        self.grid = make_grid("grid", 10, 10, 20, 10)
        self.grid.setPos(0, 0, 0)
        self.grid.reparentTo(self.render)
        self.init_skybox()
        self.taskMgr.add(self.camera_task, "cameraTask")
    
    def camera_task(self, task):
        #re-center skybox after every camera move
        camPos = camera.getPos(render)
        self.skybox.setPos(camPos)
        return Task.cont
    
    def init_skybox(self):
        skybox = self.loader.loadModel("skybox/skybox.egg")
        skybox.setScale(512) 
        skybox.setBin('background', 1) 
        skybox.setDepthWrite(0) 
        skybox.setLightOff() 
        skybox.reparentTo(self.render)
        self.skybox = skybox

app = MyApp()
app.run()

