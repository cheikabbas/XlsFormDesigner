import wx
from gui_home import Home

if __name__ == "__main__":
    app = wx.App(False)
    frame = Home()
    app.MainLoop()