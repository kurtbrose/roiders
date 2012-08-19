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

        container_panel = wx.Panel(parent=self)
        tool_panel = wx.Panel(parent=self)
        info_panel = wx.Panel(parent=container_panel)
        panda_panel = EmbeddedPandaWindow(
            parent=container_panel, pos=(0,0), style=wx.SUNKEN_BORDER)
        wx.StaticText(info_panel, -1, "INFO PANEL", (10, 10))
        
        tools_selector = wx.Notebook(parent=tool_panel)
        dig_tools = wx.Panel(tools_selector)
        wx.StaticText(dig_tools, -1, "Dig Tools", (20, 20))
        build_tools = wx.Panel(tools_selector)
        wx.StaticText(build_tools, -1, "Build Tools", (20, 20))
        tools_selector.AddPage(dig_tools, "Dig Tools")
        tools_selector.AddPage(build_tools, "Build Tools")
        tools_sizer = wx.BoxSizer()
        tools_sizer.Add(tools_selector, 1, wx.EXPAND)
        tool_panel.SetSizer(tools_sizer)
        

        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_sizer.Add(panda_panel, 9, wx.EXPAND, 0)
        horizontal_sizer.Add(info_panel, 1, wx.EXPAND, 0)
        container_panel.SetSizer(horizontal_sizer)

        vertical_sizer.Add(container_panel, 8, wx.EXPAND, 0)
        vertical_sizer.Add(tool_panel, 2, wx.EXPAND, 0)
        self.SetSizer(vertical_sizer)
        vertical_sizer.Fit(self)
        self.Layout()

        filemenu = wx.Menu()

        filemenu.Append(
            wx.ID_ABOUT, "&About", " Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)
        self.Show(True)

if __name__ == "__main__":
    mw = MainWindow()
    base.setup()
    base.run()
