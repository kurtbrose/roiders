from direct.showbase import ShowBase
from direct.task import Task
from direct.gui.DirectGui import *
from pandac import PandaModules as PM
from direct.interval.IntervalGlobal import Parallel

#for now: one "turn" = 0.3 seconds
#at the end of each turn, 

class App(ShowBase.ShowBase):
    def __init__(self):
        ShowBase.ShowBase.__init__(self)
        import resource
        resource.init(self)
        import asteroid
        import creatures
        
        self.init_skybox()
        self.init_ui()
        self.taskMgr.add(self.camera_task, "cameraTask")
        rocks = asteroid.TileType(resource.TEXTURES.rocks)
        self.asteroid = asteroid.Asteroid.make_spheroid(rocks)
        self.asteroid.nodepath.reparentTo(self.render)

        import random
        creatures = sum([[c() for i in range(100)] 
            for c in (creatures.Human, creatures.Robot)], []) 
        intervals = []
        for robot in creatures:
            robot.nodepath.reparentTo(self.render)
            robot.nodepath.setPos(random.random()*100, random.random()*100, 30)
            goto = PM.Point3(
                random.random()*1000, 
                random.random()*1000, 
                random.random()*1000)
            intervals.append(robot.nodepath.posInterval(10.0, goto))
        Parallel(*intervals, name="move_robots").start()


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
    

app = App()
#PM.PStatClient.connect()
app.run()

