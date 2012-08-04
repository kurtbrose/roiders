import itertools
import random

from direct.showbase import ShowBase
from direct.task import Task
from direct.gui.DirectGui import *
from pandac import PandaModules as PM
from direct.interval.IntervalGlobal import Parallel

#for now: one "turn" = 0.3 seconds
#at the end of each turn, 
TURN_LEN = 0.3

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
        self.asteroid = asteroid.Asteroid.make_spheroid(asteroid.Rock)
        asteroid.tunnel(self.asteroid)
        self.asteroid.nodepath.reparentTo(self.render)

        self.creatures = sum([[c() for i in range(50)] 
            for c in (creatures.Human, creatures.Robot)], []) 
        for creature in self.creatures:
            creature.pos = (0, 0, 0)
            creature.nodepath.reparentTo(self.render)

        self.start()

    def start(self):
        self.taskMgr.doMethodLater(TURN_LEN, self.do_turn, 'do_turn')

    def do_turn(self, task):
        moves = []
        for creature in self.creatures:
            if not creature.cur_path:
                x = random.randint(0, 25)
                y = random.randint(0, 25)
                z = random.randint(0, 13)
                tile = self.asteroid.get(x,y,z)
                if tile and tile.passable:
                    creature.goto((x,y,z), self.asteroid)
            if creature.cur_path:
                next = creature.cur_path.pop()
                moves.append(creature.nodepath.posInterval(TURN_LEN, 
                    self.asteroid.get_pos(*next)))
                creature.pos = next
        if moves:
            Parallel(*moves, name="creature_moves").start()
        return Task.again

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

