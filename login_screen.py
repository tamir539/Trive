import wx

class LoginPanel(wx.Panel):
    def __init__(self, parent, frame):

        #create a new panel
        wx.Panel.__init__(self, parent, pos = wx.DefaultPosition, size = (500,500), style = wx.SIMPLE_BORDER)

        self.frame = frame
        self.parent = parent
        self.__create_screen()



    def __create_screen(self):
        # create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        title = wx.StaticText(self, -1, label="Login Panel")
        titlefont = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        title.SetForegroundColour(wx.WHITE)
        title.SetFont(titlefont)

