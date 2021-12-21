import wx


class MyFrame(wx.Frame):
    def __init__(self, parent=None):
        super(MyFrame, self).__init__(parent, title="Trive", size=(500,500))
        # create status bar
        self.CreateStatusBar(1)
        self.SetStatusText("Developed by Tamir Burstein")
        # create main panel - to put on the others panels
        main_panel = MainPanel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(main_panel, 1, wx.EXPAND)
        # arrange the frame
        self.SetSizer(box)
        self.Layout()
        self.Show()

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.frame = parent
        self.SetBackgroundColour(wx.BLACK)
        self.v_box = wx.BoxSizer()

        # create object for each panel
        self.login = LoginPanel(self, self.frame)
        #self.registration = RegistrationPanel(self, self.frame)
        #self.files = FilesPanel(self,self.frame)

        self.v_box.Add(self.login)
        #self.v_box.Add(self.registration)
        #self.v_box.Add(self.files)

        # The first panel to show
        self.login.Show()
        self.SetSizer(self.v_box)
        self.Layout()

class LoginPanel(wx.Panel):
    '''
        class that create the login layout
    '''
    def __init__(self, parent, frame):

        #create a new panel
        wx.Panel.__init__(self, parent, pos = wx.DefaultPosition, size = (500,500), style = wx.SIMPLE_BORDER)

        self.frame = frame
        self.parent = parent
        self.__create_screen__()

    def __create_screen__(self):
        # create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        #create the title of the layout
        title = wx.StaticText(self, -1, label="Login Panel")
        titlefont = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        title.SetForegroundColour(wx.GREEN)
        title.SetFont(titlefont)

        #create sizer for the username
        nameBox = wx.BoxSizer(wx.HORIZONTAL)

        nameText = wx.StaticText(self, 1, label="UserName: ")
        self.userNameField = wx.TextCtrl(self, -1, name="username",size = (150, -1))
        nameBox.Add(nameText, 0, wx.ALL, 5)
        nameBox.Add(self.userNameField, 0, wx.ALL, 5)

        #create sizer for the password
        passBox = wx.BoxSizer(wx.HORIZONTAL)

        passText = wx.StaticText(self, 1, label="Password: ")
        self.passWordField = wx.TextCtrl(self, -1, name="password",style = wx.TE_PASSWORD, size = (150, -1))
        passBox.Add(passText, 0, wx.ALL, 5)
        passBox.Add(self.passWordField, 0, wx.ALL, 5)

        # login & registration buttons
        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        loginBtn = wx.Button(self, wx.ID_ANY, label="login",size=(100, 40))
        loginBtn.Bind(wx.EVT_BUTTON, self.handle_login)
        btnBox.Add(loginBtn, 0, wx.ALL, 5)

        regBtn = wx.Button(self, wx.ID_ANY, label="Registration",size = (100, 40))
        regBtn.Bind(wx.EVT_BUTTON, self.handle_reg)
        btnBox.Add(regBtn, 1, wx.ALL, 5)

        # add all elements to sizer
        self.sizer.Add(title, 0, wx.CENTER | wx.TOP, 5)
        self.sizer.AddSpacer(10)
        self.sizer.Add(nameBox,0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(passBox,-1, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(10)
        self.sizer.Add(btnBox, wx.CENTER | wx.ALL, 5)

        # arrange the screen
        self.SetSizer(self.sizer)
        self.Layout()
        self.Hide()

    def handle_login(self, event):
        '''

        :param event:event that happend on the screen
        :return:take care the event when pressing login button
        '''
        username = self.userNameField.GetValue()
        password = self.passWordField.GetValue()

        if not username or not password :
            self.frame.SetStatusText("Must enter name and password")
        else:
            self.frame.SetStatusText("waiting for Server approve")

    def handle_reg(self,event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        self.frame.SetStatusText("")
        self.Hide()
        self.parent.registration.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()