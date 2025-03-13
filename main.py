import wx
from gui_home import Home

if __name__ == "__main__":
    ICON_PATH = "img/xlsform-designer-icon.ico"
    app = wx.App(False)
    frame = Home()
    frame.SetIcon(wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO))
    app.MainLoop()