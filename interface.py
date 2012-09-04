import math
import os, os.path

CUR_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
ASSET_DIR = CUR_DIR + 'assets/'
ICON_DIR = ASSET_DIR + 'icons/'

import wx

from pandac.PandaModules import Quat
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

        info_sizer = wx.GridSizer(5,1,3,3)
        info_sizer.Add(wx.StaticText(info_panel, -1, "INFO PANEL"))
        info_sizer.Add(CameraControlPanel(info_panel, base))
        info_panel.SetSizer(info_sizer)
        
        tools_selector = wx.Notebook(parent=tool_panel)
        dig_tools = ToolsPanel(tools_selector, [Tool(None, "dig", "dig")])
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

TOOL_PANEL_SCALE = 32
TPS = TOOL_PANEL_SCALE

class ToolsPanel(wx.Panel):
    def __init__(self, parent, tools):
        wx.Panel.__init__(self, parent)
        self.selected_tool = tools[0]
        self.tools = tools
        tools_sizer = wx.GridSizer(2, int(math.ceil(len(tools)/2.0)), TPS, TPS)

        for tool in tools:
            tool_button = wx.ToggleButton(
                self, -1, size=(TPS,TPS), label=tool.name)
            tool_button.SetToolTip(wx.ToolTip(tool.tooltip))
            tools_sizer.Add(tool_button, 1)

        self.SetSizer(tools_sizer)
        
class Tool(object):
    'A simple, library-agnostic value-object class'
    def __init__(self, icon, name, tooltip):
        #TODO: wire this up to the code for doing stuff
        self.icon = icon
        self.name = name
        self.tooltip = tooltip

POS_SCALE = 30.0
ROT_SCALE = 2.5

def hpr2quat(h,p,r):
    q = Quat()
    q.setHpr((h,p,r))
    return q

class CameraControlPanel(wx.Panel):
    def __init__(self, parent, panda_app):
        wx.Panel.__init__(self, parent)

        self.panda_app = panda_app

        mk_btn = lambda icon: wx.BitmapButton(
            self, -1, wx.Bitmap(ICON_DIR+'arrow_'+icon+'.png'))

        self.up = mk_btn('up')
        self.down = mk_btn('down')
        self.left = mk_btn('left')
        self.right = mk_btn('right')
        self.roll_left = mk_btn('rotate_anticlockwise')
        self.roll_right = mk_btn('rotate_clockwise')

        sizer = wx.GridSizer(6, 3, 1, 1)
        #row 1
        sizer.Add(self.roll_left)
        sizer.Add(self.up)
        sizer.Add(self.roll_right)
        #row 2
        sizer.Add(self.left)
        sizer.Add(wx.StaticText(self, -1, "ROT"))
        sizer.Add(self.right)
        #row 3
        sizer.Add(wx.Panel(self))
        sizer.Add(self.down)
        sizer.Add(wx.Panel(self))

        self.go_fwd = mk_btn('in')
        self.go_back = mk_btn('out')
        self.go_up = mk_btn('up')
        self.go_down = mk_btn('down')
        self.go_left = mk_btn('left')
        self.go_right = mk_btn('right')

        #row 4
        sizer.Add(self.go_fwd)
        sizer.Add(self.go_up)
        sizer.Add(self.go_back)
        #row 5
        sizer.Add(self.go_left)
        sizer.Add(wx.StaticText(self, -1, "POS"))
        sizer.Add(self.go_right)
        #row 6
        sizer.Add(wx.Panel(self))
        sizer.Add(self.go_down)
        sizer.Add(wx.Panel(self))

        self.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.on_click)
        self.rotations = { 
            self.up         : hpr2quat(0, ROT_SCALE,0),
            self.down       : hpr2quat(0,-ROT_SCALE,0),
            self.left       : hpr2quat( ROT_SCALE,0,0),
            self.right      : hpr2quat(-ROT_SCALE,0,0),
            self.roll_left  : hpr2quat(0,0,-ROT_SCALE),
            self.roll_right : hpr2quat(0,0, ROT_SCALE),
        }

        self.positions = { 
            self.go_fwd   : (0, POS_SCALE,0),
            self.go_back  : (0,-POS_SCALE,0),
            self.go_up    : (0,0, POS_SCALE),
            self.go_down  : (0,0,-POS_SCALE),
            self.go_left  : (-POS_SCALE,0,0),
            self.go_right : ( POS_SCALE,0,0),
        }

    #TODO: why does the collision not move when the camera does?
    def on_click(self, event):
        pc = self.panda_app.cam
        pc2 = self.panda_app.picker_node_path
        src = event.GetEventObject()

        rot = self.rotations.get(src)
        if rot: #note: quaternion multiplication not commmutative
            pc.setQuat(pc.getQuat() * rot)
            pc2.setQuat(pc.getQuat() * rot)

        pos = self.positions.get(src)
        if pos:
            pc.setPos(pc.getPos() + pos)
            pc2.setPos(pc.getPos() + pos)

        #import pdb; pdb.set_trace()



if __name__ == "__main__":
    mw = MainWindow()
    base.setup()
    base.run()
