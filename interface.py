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

#copied from Panda library
class EmbeddedPandaWindow(wx.Window):
    """ This class implements a Panda3D window that is directly
    embedded within the frame.  It is fully supported on Windows,
    partially supported on Linux, and not at all on OSX. """

    def __init__(self, *args, **kw):
        gsg = None
        if 'gsg' in kw:
            gsg = kw['gsg']
            del kw['gsg']

        base.startWx()
        wx.Window.__init__(self, *args, **kw)

        wp = WindowProperties.getDefault()
        if platform.system() != 'Darwin':
            try:
                wp.setParentWindow(self.GetHandle())
            except OverflowError:
                # Sheesh, a negative value from GetHandle().  This can
                # only happen on 32-bit Windows.
                wp.setParentWindow(self.GetHandle() & 0xffffffff)

        self.win = base.openWindow(props = wp, gsg = gsg, type = 'onscreen',
                                   unexposedDraw = False)
        self.Bind(wx.EVT_SIZE, self.onSize)

        # This doesn't actually do anything, since wx won't call
        # EVT_CLOSE on a child window, only on the toplevel window
        # that contains it.
        self.Bind(wx.EVT_CLOSE, self.__closeEvent)

    def __closeEvent(self, event):
        self.cleanup()
        event.Skip()

    def cleanup(self):
        """ Parent windows should call cleanup() to clean up the
        wxPandaWindow explicitly (since we can't catch EVT_CLOSE
        directly). """
        if self.win:
            base.closeWindow(self.win)
            self.win = None

    def onSize(self, event):
        wp = WindowProperties()
        wp.setOrigin(0, 0)
        wp.setSize(*self.GetClientSize())
        self.win.requestProperties(wp)
        event.Skip()

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

from pandac.PandaModules import MouseWatcher

print "mouseWatcherNode", base.mouseWatcherNode
print "mouseInterfaceNode", base.mouseInterfaceNode
print "pointerWatcherNodes", base.pointerWatcherNodes
#base.enableMouse()
#base.mouseWatcherNode = base.render.attachNewNode(MouseWatcher())
print "mouseWatcherNode", base.mouseWatcherNode

#trying to get to the bottom of window events not propagating
base.taskMgr.doMethodLater(3.0, lambda task: base.messenger.send('b'), 'testb')
#base.taskMgr.doMethodLater(3.0, lambda task: base.messenger.send('a'), 'testa')
base.taskMgr.doMethodLater(3.0, lambda task: base.messenger.send('c'), 'testc')

base.run()


