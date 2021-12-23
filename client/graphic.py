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
        png = wx.Image('draws\\logo.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        trive = wx.StaticBitmap(self, -1, png, (650, -2), (png.GetWidth(), png.GetHeight()))

        #font for static text
        font = wx.Font(22, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        #create sizer for the username
        nameBox = wx.BoxSizer(wx.HORIZONTAL)
        self.userNameField = wx.TextCtrl(self, -1, name="username", size = (500 ,38))
        self.userNameField.SetBackgroundColour(wx.BLACK)
        self.userNameField.SetForegroundColour(wx.WHITE)
        self.userNameField.Font = font
        # add the user logo
        user = wx.Image('draws\\user.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        user_logo = wx.StaticBitmap(self, -1, user, (565, 275), (user.GetWidth(), user.GetHeight()))
        nameBox.Add(user_logo, 0, wx.ALL, 0)
        nameBox.Add(self.userNameField, 0, wx.ALL, 0)

        #create sizer for the password
        passBox = wx.BoxSizer(wx.HORIZONTAL)
        self.passWordField = wx.TextCtrl(self, -1, name="password",style = wx.TE_PASSWORD, size = (500, 38))
        self.passWordField.SetBackgroundColour(wx.BLACK)
        self.passWordField.SetForegroundColour(wx.WHITE)
        self.passWordField.SetFont(font)
        # add the fingerprint logo
        finger = wx.Image('draws\\finger.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        finger_logo = wx.StaticBitmap(self, -1, finger, (565, 383), (finger.GetWidth(), finger.GetHeight()))
        passBox.Add(finger_logo, 0, wx.ALL, 0)
        passBox.Add(self.passWordField, 0, wx.ALL, 5)

        #login & registration buttons
        loginBtn = wx.Button(self, wx.ID_ANY, label="login", size=(400, 40))
        loginBtn.Font = font.Bold()
        loginBtn.BackgroundColour = wx.BLACK
        loginBtn.ForegroundColour = wx.GREEN
        loginBtn.Refresh()
        loginBtn.Bind(wx.EVT_BUTTON, self.handle_login)

        regBtn = wx.Button(self, wx.ID_ANY, label="not a member? sign up!",size = (400, 40))
        regBtn.Font = font
        regBtn.BackgroundColour = wx.BLACK
        regBtn.ForegroundColour = wx.GREEN
        regBtn.Bind(wx.EVT_BUTTON, self.handle_reg)

        #size down the font for the forgot your password button
        font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        forgotBtn = wx.Button(self, wx.ID_ANY, label="forgot your password?", size=(250, 30))
        forgotBtn.Font = font.MakeUnderlined()
        forgotBtn.BackgroundColour = wx.BLACK
        forgotBtn.ForegroundColour = wx.GREEN
        forgotBtn.Bind(wx.EVT_BUTTON, self.handle_forgot_password)

        # add all elements to sizer
        self.sizer.Add(trive,0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(100)
        self.sizer.Add(nameBox,0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(passBox,0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(20)
        self.sizer.Add(loginBtn, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(regBtn,0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(forgotBtn, 0, wx.CENTER | wx.ALL, 5)

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

    def handle_forgot_password(self,event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing forgot password
        '''
        #self.Hide()
        pass


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
        png = wx.Image('draws\\logo.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        logo = wx.StaticBitmap(self, -1, png, (650, -2), (png.GetWidth(), png.GetHeight()))


        # font for static text
        font = wx.Font(22, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        # font for input
        font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        # create sizer for the username
        nameBox = wx.BoxSizer(wx.HORIZONTAL)

        self.userNameField = wx.TextCtrl(self, 10, name="username", style=wx.TEXT_ATTR_BULLET_STYLE_ROMAN_UPPER,size=(500, 38))
        self.userNameField.SetBackgroundColour(wx.BLACK)
        self.userNameField.SetForegroundColour(wx.WHITE)
        self.userNameField.Font = font

        # add the user logo
        user = wx.Image('draws\\user.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        user_logo = wx.StaticBitmap(self, -1, user, (565, 275), (user.GetWidth(), user.GetHeight()))

        nameBox.Add(user_logo, 0, wx.ALL, 0)
        nameBox.Add(self.userNameField, 0, wx.ALL, 5)

        # create sizer for the email
        emailBox = wx.BoxSizer(wx.HORIZONTAL)

        self.emailField = wx.TextCtrl(self, -1, name="email", size=(500, 38))
        self.emailField.SetFont(font)
        self.emailField.SetBackgroundColour(wx.BLACK)
        self.emailField.SetForegroundColour(wx.WHITE)
        # add the email logo
        email = wx.Image('draws\\email.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        email_logo = wx.StaticBitmap(self, -1, email, (565, 275), (email.GetWidth(), email.GetHeight()))

        emailBox.Add(email_logo, 0, wx.ALL, 0)
        emailBox.Add(self.emailField, 0, wx.ALL, 0)

        # create sizer for the password
        passBox = wx.BoxSizer(wx.HORIZONTAL)

        self.passWordField = wx.TextCtrl(self, -1, name="password", style=wx.TE_PASSWORD, size=(500, 38))
        self.passWordField.SetBackgroundColour(wx.BLACK)
        self.passWordField.SetForegroundColour(wx.WHITE)
        self.passWordField.SetFont(font)

        # add the fingerprint logo
        finger = wx.Image('draws\\finger.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        finger_logo = wx.StaticBitmap(self, -1, finger, (565, 383), (finger.GetWidth(), finger.GetHeight()))

        passBox.Add(finger_logo, 0, wx.ALL, 0)
        passBox.Add(self.passWordField, 0, wx.ALL, 5)

        #registration and login buttons

        regBtn = wx.Button(self, wx.ID_ANY, label="register", size=(400, 40))
        regBtn.Font = font.Bold()
        regBtn.BackgroundColour = wx.BLACK
        regBtn.ForegroundColour = wx.GREEN
        regBtn.Bind(wx.EVT_BUTTON, self.handle_reg)

        font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        loginBtn = wx.Button(self, wx.ID_ANY, label="login", size=(250, 30))
        loginBtn.Font = font
        loginBtn.BackgroundColour = wx.BLACK
        loginBtn.ForegroundColour = wx.GREEN
        loginBtn.Bind(wx.EVT_BUTTON, self.handle_login)
        # btnBox.Add(regBtn, 1, wx.ALL, 5)
        # add all elements to sizer

        self.sizer.Add(logo, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(100)
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