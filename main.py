import wx
from gui import Home

if __name__ == "__main__":
    app = wx.App(False)
    frame = Home()
    app.MainLoop()