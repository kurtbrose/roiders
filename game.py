import os, os.path

from panda3d.core import Filename
from panda3d import core

from direct.showbase import ShowBase
from direct.showbase import Loader
from direct.task import Task
from direct.gui.DirectGui import *
from direct.filter.CommonFilters import CommonFilters

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

class RockSlabFactory(object):
    def __init__(self, app):
        self.app = app
        self.texture = app.loader.loadTexture('rocks.png')
        self.card_maker = PM.CardMaker('rock_slab_gen')
    
    def make_slab(self, width, height):
        self.card_maker.setFrame(0, width, 0, height)
        slab = self.app.render.attachNewNode(self.card_maker.generate())
        slab.setTexture(self.texture)
        slab.setTwoSided(True) #visible from both sides; no back-face culling
        return slab
    
    def make_stack(self, width, height, spacing, num):
        stack = PandaNode('stack')
        stack_node_path = NodePath(stack)
        for i in range(num):
            cur_slab = self.make_slab(width, height)
            cur_slab.reparentTo(stack_node_path)
            cur_slab.setY(i*spacing)
        stack_node_path.reparentTo(self.app.render)
        return stack_node_path

class App(ShowBase.ShowBase):
    def __init__(self):
        ShowBase.ShowBase.__init__(self)
        self.grid = make_grid("grid", 10, 10, 20, 10)
        self.grid.setPos(0, 0, 0)
        self.grid.reparentTo(self.render)
        
        self.rock_fact = RockSlabFactory(self)
        self.rock_fact.make_stack(30, 30, 5, 20)
        
        self.init_skybox()
        self.init_ui()
        self.init_shaders()
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
    
    def init_ui(self):
        self.test_button = DirectButton(
            text = ("ok!", "click!", "rolling over", "disabled"),
            scale = 0.05)
        self.test_button.setPos(base.a2dLeft, 0, base.a2dTop)
    
    def init_shaders(self):
        self.filters = CommonFilters(base.win, base.cam)
        ok = self.filters.setBloom(blend=(0,0,0,1),
                                   desat=-0.5,
                                   intensity=3.0,
                                   size="small")
        if not ok:
            print "info: graphics card does not support shaders"

app = App()
app.run()

