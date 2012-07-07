from direct.showbase import ShowBase
from pandac.PandaModules import OrthographicLens
from pandac.PandaModules import LineSegs
#draw a grid


def draw_grid(name, rows, cols, size, thickness):
    lines = LineSegs()
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
    node = PandaNode(name)
    

class MyApp(ShowBase.ShowBase):
    def __init__(self):
        ShowBase.ShowBase.__init__(self)
        
        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)
        
        
        lens = OrthographicLens()
        lens.setFilmSize(20, 15)
        self.cam.node().setLens(lens)

app = MyApp()
app.run()

