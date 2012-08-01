import os
import os.path
from panda3d.core import Filename
from pandac import PandaModules as PM

#set up some loading constants
DIR = str(Filename.fromOsSpecific(os.path.dirname(os.path.abspath(__file__))))
#convert back to base string from panda type
ASSET_DIR = DIR + "/assets/"
PM.getModelPath().appendPath(ASSET_DIR)


class TextureManager(object):
    def __init__(self, app):
        self.rocks = app.loader.loadTexture('rocks.png')

        for icon in ['arrow_out', 'asterisk_orange', 'bug', 'user']:
            setattr(self, icon,
                app.loader.loadTexture('icons/' + icon + '.png'))

TEXTURES = None


def init(app):
    global TEXTURES
    TEXTURES = TextureManager(app)
