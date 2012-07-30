import os, os.path
import math

from panda3d.core import Filename
from panda3d import core

from direct.showbase import ShowBase
from direct.showbase import Loader
from direct.task import Task
from direct.gui.DirectGui import *
from direct.filter.CommonFilters import CommonFilters

from pandac import PandaModules as PM
from pandac.PandaModules import PandaNode
from pandac.PandaModules import NodePath

import asteroid

#set up some loading constants
DIR = str(Filename.fromOsSpecific(os.path.dirname(os.path.abspath(__file__))))
#convert back to base string from panda type
ASSET_DIR = DIR+"/assets/"
PM.getModelPath().appendPath(ASSET_DIR) 

class TextureManager(object):
    def __init__(self, app):
        self.arrow_out = app.loader.loadTexture('icons/arrow_out.png')
        self.rocks = app.loader.loadTexture('rocks.png')

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
    
    def make_spheroid_stack(self, radius, num, name='stack'):
        spacing = radius / (num - 2)
        stack = PandaNode(name)
        stack_node_path = NodePath(stack)
        for i in range(num):
            cur_radius = radius*math.sin(math.acos( abs(1 - i*2.0/num) ))
            cur_slab = self.make_slab(cur_radius, cur_radius)
            cur_slab.reparentTo(stack_node_path)
            #offset to center smaller items in sphere
            offset = (radius - cur_radius)/2.0
            cur_slab.setPos(offset, i*spacing, offset)
        stack_node_path.reparentTo(self.app.render)
        return stack_node_path


class App(ShowBase.ShowBase):
    def __init__(self):
        ShowBase.ShowBase.__init__(self)
        
        self.rock_fact = RockSlabFactory(self)
        self.tex_mgr = TextureManager(self)
        
        '''
        for i in range(2):
            a = self.rock_fact.make_spheroid_stack(100, 20, "name"+str(i))
            a.setPos(150*i, 0, 0)
            a.flattenStrong()
        '''

        self.init_skybox()
        self.init_ui()
        #self.init_shaders()
        self.taskMgr.add(self.camera_task, "cameraTask")
        arrowout = asteroid.TileType(self.tex_mgr.arrow_out)
        rocks = asteroid.TileType(self.tex_mgr.rocks)
        a = asteroid.Asteroid.make_spheroid(arrowout)
        a.nodepath.reparentTo(self.render)
        '''
        for i in range(a.width):
            for j in range(a.height):
                for k in range(a.depth):
                    a.update(i, j, k, arrowout)
        a.redraw()
        '''

        import random
        def replace_random(task):
            for i in range(20):
                x = random.randint(0, a.width-1)
                y = random.randint(0, a.height-1)
                z = random.randint(0, a.depth-1)
                a.update(x, y, z, rocks)
            a.redraw()
            return task.again
        self.taskMgr.doMethodLater(0.3, replace_random, 'replace_random')
        '''
        for i in range(25):
            self.replace_random_test(100*i)
        '''

    def replace_random_test(self, y):
        SIZE = 25
        np = NodePath(PandaNode('billboard'))
        np.reparentTo(self.render)
        #np.setPos(0, -1000, 0)
        s1 = self.rock_fact.make_slab(10, 10)
        s2 = self.rock_fact.make_slab(10, 10)
        s2.setTexture(self.tex_mgr.arrow_out)
        nodes = []
        import time
        a = time.time()
        for i in range(SIZE*SIZE):
            cur = s1.copyTo(np) if i%2 else s2.copyTo(np)
            cur.setPos(200+10*(i%SIZE), y, 200+10*(i/SIZE))
            nodes.append(cur)
            #s.setTransparency(True)
        print time.time() - a
        #np.flattenMedium()
        print time.time() - a

        '''
        eraser = TextureStage('eraser')
        #eraser.setSort(1)
        eraser.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSConstant, TextureStage.COSrcAlpha)
        eraser.setCombineRgb(TextureStage.CMAdd, TextureStage.CSTexture , TextureStage.COSrcColor, 
                                                 TextureStage.CSPrevious, TextureStage.COSrcColor)
        eraser.setColor(Vec4(0, 0, 0, 0.5))
        blank = PNMImage(1,1)
        blank.fillVal(0,0,0)
        blanktex = Texture()
        blanktex.load(blank)
        '''
        import random
        def replace_random(task):
            for i in range(20):
                num = random.choice(range(SIZE*SIZE))
                nodes[num].setTexture(self.tex_mgr.arrow_out if random.random() > 0.5 else self.rock_fact.texture)
                '''
                cur = s1.copyTo(np) if random.random() > 0.5 else s2.copyTo(np)
                cur.setPos(200 +10*(num%SIZE), y, 200+10*(num/SIZE))
                '''
                #TODO: what is wrong with coordinates?  what are these drawing in different location than initial slabs?
                #s.setTransparency(True)
            #np.flattenMedium()
            #np.setTransparency(True)
            #np.setTexture(eraser, blanktex)
            return task.again

        if y < 500:
            self.taskMgr.doMethodLater(0.3, replace_random, 'replace_random')


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
        ok = self.filters.setBloom(#blend=(0,0,0,1),
                                   desat=-0.5,
                                   intensity=0.45,
                                   size="medium")
        if not ok:
            print "info: graphics card does not support shaders"

app = App()
#PM.PStatClient.connect()
app.run()

