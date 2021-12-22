import wx


class MyFrame(wx.Frame):
    def __init__(self, parent=None):
        super(MyFrame, self).__init__(parent, title="Trive", size=(1920,1080))
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
        self.registration = RegisterPanel(self, self.frame)
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
        wx.Panel.__init__(self, parent, pos = wx.DefaultPosition, size = (1920,1080), style = wx.SIMPLE_BORDER)

        self.frame = frame
        self.parent = parent
        self.__create_screen__()

    def __create_screen__(self):
        # create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # change background colour to black
        self.SetBackgroundColour(wx.BLACK)


        #add the Trive logo
        png = wx.Image('logo.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(self, -1, png, (650, -2), (png.GetWidth(), png.GetHeight()))

        #font for static text
        font = wx.Font(22, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        #font for input
        inp_font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        #create sizer for the username
        nameBox = wx.BoxSizer(wx.HORIZONTAL)

        nameText = wx.StaticText(self, 1, label="UserName: ")
        nameText.SetFont(font)
        self.userNameField = wx.TextCtrl(self, 10, name="username", style = wx.TEXT_ATTR_BULLET_STYLE_ROMAN_UPPER, size = (300 ,45))
        self.userNameField.SetBackgroundColour(wx.BLACK)
        self.userNameField.SetForegroundColour(wx.WHITE)
        self.userNameField.Font = inp_font
        nameText.SetForegroundColour(wx.GREEN)
        nameBox.Add(nameText, 10, wx.ALL, 5)
        nameBox.Add(self.userNameField, 0, wx.ALL, 0)


        #create sizer for the password
        passBox = wx.BoxSizer(wx.HORIZONTAL)

        passText = wx.StaticText(self, 1, label="Password: ")
        passText.SetFont(font)

        self.passWordField = wx.TextCtrl(self, -1, name="password",style = wx.TE_PASSWORD, size = (300, 45))
        self.passWordField.SetBackgroundColour(wx.BLACK)
        self.passWordField.SetForegroundColour(wx.WHITE)
        self.passWordField.SetFont(inp_font)
        passText.SetForegroundColour(wx.GREEN)
        passBox.Add(passText, 0, wx.ALL, 5)
        passBox.Add(self.passWordField, 0, wx.ALL, 5)

        # # login & registration buttons
        # btnBox = wx.BoxSizer(wx.HORIZONTAL)

        loginBtn = wx.Button(self, wx.ID_ANY, label="login", size=(400, 40))
        loginBtn.Font = font
        loginBtn.BackgroundColour = wx.BLACK
        loginBtn.DisableFocusFromKeyboard()
        loginBtn.ForegroundColour = wx.GREEN
        loginBtn.Refresh()
        loginBtn.Bind(wx.EVT_BUTTON, self.handle_login)
        #btnBox.Add(loginBtn, 0, wx.ALL, 5)

        regBtn = wx.Button(self, wx.ID_ANY, label="not a member? sign up!",size = (400, 40))
        regBtn.Font = font
        regBtn.BackgroundColour = wx.BLACK
        regBtn.ForegroundColour = wx.GREEN
        regBtn.Bind(wx.EVT_BUTTON, self.handle_reg)
        #btnBox.Add(regBtn, 1, wx.ALL, 5)

        # add all elements to sizer

        self.sizer.AddSpacer(275)
        self.sizer.Add(nameBox,0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(passBox,0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(20)
        #self.sizer.Add(btnBox, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(loginBtn, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(regBtn,0, wx.CENTER | wx.ALL, 5)

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
            pass
            #self.frame.SetStatusText("Must enter name and password")
        else:
            pass
            #self.frame.SetStatusText("waiting for Server approve")

    def handle_reg(self,event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        self.Hide()
        self.parent.registration.Show()

class RegisterPanel(wx.Panel):
    '''
        class that create the register layout
    '''

    def __init__(self, parent, frame):

        # create a new panel
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, size=(1920, 1080), style=wx.SIMPLE_BORDER)

        self.frame = frame
        self.parent = parent
        self.__create_screen__()

    def __create_screen__(self):
        # create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        # add the Trive logo
        png = wx.Image('logo.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(self, -1, png, (650, -2), (png.GetWidth(), png.GetHeight()))

        # font for static text
        font = wx.Font(22, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        # font for input
        inp_font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        # create sizer for the username
        nameBox = wx.BoxSizer(wx.HORIZONTAL)

        nameText = wx.StaticText(self, 1, label="UserName: ")
        nameText.SetFont(font)
        self.userNameField = wx.TextCtrl(self, 10, name="username", style=wx.TEXT_ATTR_BULLET_STYLE_ROMAN_UPPER,size=(300, 45))
        self.userNameField.SetBackgroundColour(wx.BLACK)
        self.userNameField.SetForegroundColour(wx.WHITE)
        self.userNameField.Font = inp_font
        nameText.SetForegroundColour(wx.GREEN)
        nameBox.Add(nameText, 0, wx.ALL, 0)
        nameBox.Add(self.userNameField, 0, wx.ALL, 5)

        # create sizer for the email
        emailBox = wx.BoxSizer(wx.HORIZONTAL)

        emailText = wx.StaticText(self, 1, label="Email: ")
        self.emailField = wx.TextCtrl(self, -1, name="email", size=(300, 45))
        self.emailField.SetFont(inp_font)
        self.emailField.SetBackgroundColour(wx.BLACK)
        self.emailField.SetForegroundColour(wx.WHITE)
        emailText.SetForegroundColour(wx.GREEN)
        emailText.SetFont(font)
        emailBox.Add(emailText, 0, wx.ALL, 0)
        emailBox.Add(self.emailField, 0, wx.ALL, 5)

        # create sizer for the password
        passBox = wx.BoxSizer(wx.HORIZONTAL)

        passText = wx.StaticText(self, 1, label="Password: ")
        passText.SetFont(font)

        self.passWordField = wx.TextCtrl(self, -1, name="password", style=wx.TE_PASSWORD, size=(300, 45))
        self.passWordField.SetBackgroundColour(wx.BLACK)
        self.passWordField.SetForegroundColour(wx.WHITE)
        self.passWordField.SetFont(inp_font)
        passText.SetForegroundColour(wx.GREEN)

        passBox.Add(passText, 0, wx.ALL, 0)
        passBox.Add(self.passWordField, 0, wx.ALL, 5)

        #registration and login buttons

        regBtn = wx.Button(self, wx.ID_ANY, label="register", size=(400, 45))
        regBtn.Font = font
        regBtn.BackgroundColour = wx.BLACK
        regBtn.ForegroundColour = wx.GREEN
        regBtn.Bind(wx.EVT_BUTTON, self.handle_reg)

        loginBtn = wx.Button(self, wx.ID_ANY, label="already have an account? log in!", size=(400, 45))
        loginBtn.Font = font
        loginBtn.BackgroundColour = wx.BLACK
        loginBtn.ForegroundColour = wx.GREEN
        loginBtn.Bind(wx.EVT_BUTTON, self.handle_login)
        # btnBox.Add(regBtn, 1, wx.ALL, 5)
        # add all elements to sizer

        self.sizer.AddSpacer(275)
        self.sizer.Add(emailBox, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(nameBox, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(passBox, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(20)
        # self.sizer.Add(btnBox, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(regBtn, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(loginBtn, 0, wx.CENTER | wx.ALL, 5)
        # arrange the screen
        self.SetSizer(self.sizer)
        self.Layout()
        self.Hide()

    def handle_reg(self, event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        #mean someone create account


    def handle_login(self, event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        self.Hide()
        self.parent.login.Show()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()