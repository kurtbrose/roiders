import wx

from direct.wxwidgets.WxPandaWindow import WxPandaWindow
from panda3d import core
#suppress default window, since we will use a WxPython window
core.loadPrcFileData('startup', 'window-type none') 

import game
base = game.App()
base.startWx()
#base.wxApp.Bind()

#trying to get to the bottom of window events not propagating
#base.messenger.toggleVerbose()
import sys
base.accept('a', lambda: sys.stdout.write('a\n'))
base.accept('b', lambda: sys.stdout.write('b\n'))
base.accept('c', lambda: sys.stdout.write('c\n'))

class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Test', size=(640, 480))
        self.panda_panel = WxPandaWindow(parent=self)

        filemenu = wx.Menu()

        filemenu.Append(
            wx.ID_ABOUT, "&About", " Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)
        self.Show(True)

        base.setup()

mw = MainWindow()

#trying to get to the bottom of window events not propagating
base.taskMgr.doMethodLater(3.0, lambda task: base.messenger.send('b'), 'testb')
#base.taskMgr.doMethodLater(3.0, lambda task: base.messenger.send('a'), 'testa')
base.taskMgr.doMethodLater(3.0, lambda task: base.messenger.send('c'), 'testc')

base.run()


