import random
import time

from direct.showbase import ShowBase
from direct.task import Task
from direct.gui.DirectGui import *
from pandac.PandaModules import GeomNode
from pandac.PandaModules import CollisionHandlerQueue
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionRay
from pandac.PandaModules import CollisionNode
from direct.interval.IntervalGlobal import Parallel

#for now: one "turn" = 0.3 seconds
#at the end of each turn, 
TICK_LEN = 0.1
TICK_NUM = 0
LAST_TICK = None
AVG_TICK_LEN = TICK_LEN

class App(ShowBase.ShowBase):
    def setup(self):
        'to be called after window is initialized'
        import resource
        resource.init(self)
        import asteroid
        import creatures
        
        self.init_skybox()
        self.init_ui()
        self.taskMgr.add(self.camera_task, "cameraTask")
        self.asteroid = asteroid.Asteroid.make_spheroid(asteroid.Rock, 12)
        asteroid.tunnel(self.asteroid)
        self.asteroid.nodepath.reparentTo(self.render)

        self.creatures = sum([[c() for i in range(5)] 
            for c in (creatures.Human, creatures.Robot)], []) 
        for creature in self.creatures:
            creature.pos = (0, 0, 0)
            creature.nodepath.reparentTo(self.render)

        self.start()
        self.setFrameRateMeter(True)

    def start(self):
        global LAST_TICK
        LAST_TICK = time.time()
        self.taskMgr.doMethodLater(TICK_LEN, self.do_tick, 'do_tick')

    def do_tick(self, task):
        global TICK_NUM, LAST_TICK, AVG_TICK_LEN
        TICK_NUM += 1
        cur_time = time.time()
        start_time = cur_time
        AVG_TICK_LEN = ((cur_time - LAST_TICK) + AVG_TICK_LEN)/2
        LAST_TICK = cur_time
        if TICK_NUM % 50 == 0:
            print "average tick length", AVG_TICK_LEN
        moves = []
        for creature in self.creatures:
            creature.action = (creature.action + 1) % creature.speed
            if creature.action == 0:
                continue
            if not creature.cur_path:
                x = random.randint(0, 25)
                y = random.randint(0, 25)
                z = random.randint(0, 13)
                tile = self.asteroid.get(x,y,z)
                if tile and tile.passable:
                    creature.goto((x,y,z), self.asteroid)
            if creature.cur_path:
                next = creature.cur_path.pop()
                moves.append(creature.nodepath.posInterval(
                    AVG_TICK_LEN*(creature.speed-1), 
                    self.asteroid.get_pos(*next)))
                creature.pos = next
        if moves:
            Parallel(*moves, name="creature_moves "+str(TICK_NUM)).start()
        duration = time.time() - start_time
        self.taskMgr.doMethodLater(
            max(TICK_LEN-duration, 0), self.do_tick, 'do_tick')

    def camera_task(self, task):
        #re-center skybox after every camera move
        camPos = self.camera.getPos(render)
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
        self.cTrav = CollisionTraverser('ui_collision_traverser')
        self.collision_handler = CollisionHandlerQueue()
        picker_node = CollisionNode('mouse_click_ray')
        picker_node_path = self.camera.attachNewNode(picker_node)
        picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.picker_ray = CollisionRay()
        picker_node.addSolid(self.picker_ray)
        self.cTrav.addCollider(picker_node_path, self.collision_handler)

        self.accept('a', self.mouse_ray)

        #testing input
        import sys
        self.accept('b', lambda: sys.stdout.write("b"))

    def mouse_ray(app):
        'cast a ray from the current mouse position, find intersections'
        if not app.mouseWatcherNode.hasMouse():
            return None
        mouse_pos = app.mouseWatcherNode.getMouse()
        #cast a ray from the camera
        app.picker_ray.setFromLens(app.camNode, mouse_pos.getX(), mouse_pos.getY())
        #see if it hit anything in the scene graph
        app.cTrav.traverse(app.render)
        if app.collision_handler.getNumEntries() > 0:
            #get closest collision
            app.collision_handler.sortEntries()

            for i in range(app.collision_handler.getNumEntries()):
                hit = app.collision_handler.getEntry(i)
                if app.asteroid.nodepath.isAncestorOf(hit.getIntoNodePath()):
                    x,y,z = app.asteroid.get_collision_pos(hit)
                    import asteroid
                    app.asteroid.update(x,y,z,asteroid.Empty())
                    app.asteroid.redraw()
                    break

if __name__ == '__main__':
    app = App()
    app.setup()
    app.run()
