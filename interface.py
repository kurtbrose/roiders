import wx

from direct.wxwidgets.WxPandaWindow import WxPandaWindow
from pandac.PandaModules import WindowProperties
from panda3d import core
#suppress default window, since we will use a WxPython window
core.loadPrcFileData('startup', 'window-type none') 

import game
base = game.App()
base.startWx()


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

        wx.Window.__init__(self, *args, **kw)

        wp = WindowProperties.getDefault()
        #if platform.system() != 'Darwin':
        try:
            wp.setParentWindow(self.GetHandle())
        except OverflowError:
            # Sheesh, a negative value from GetHandle().  This can
            # only happen on 32-bit Windows.
            wp.setParentWindow(self.GetHandle() & 0xffffffff)

        self.win = base.openMainWindow(props = wp, gsg = gsg, type = 'onscreen',
                                   unexposedDraw = False)
        self.Bind(wx.EVT_SIZE, self.onSize)

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
        x,y = self.GetClientSize()
        wp.setSize(x,y)
        base.camLens.setAspectRatio(1.0*y/x)
        base.win.requestProperties(wp)
        event.Skip()

class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title='roiders', size=(640, 480))

        panel = wx.Panel(self)
        fgs = wx.FlexGridSizer(2, 2, 0, 0)

        spacer = wx.StaticText(panel, label="spacer")
        button_row = wx.StaticText(panel, label="BUTTON ROW")
        button_col = wx.StaticText(panel, label="BUTTON COL")

        self.panda_panel = EmbeddedPandaWindow(
            parent=self, pos=(0,0), style=wx.SUNKEN_BORDER)

        fgs.AddMany([
            spacer, 
            (button_row, 1, wx.EXPAND), 
            button_col, 
            (self.panda_panel, 1, wx.EXPAND)])

        fgs.AddGrowableRow(1,1)
        fgs.AddGrowableCol(1,1)

        panel.SetSizer(fgs)

        filemenu = wx.Menu()

        filemenu.Append(
            wx.ID_ABOUT, "&About", " Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)
        self.Show(True)

mw = MainWindow()

base.setup()
base.run()


