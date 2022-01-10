import wx
import wx.lib.scrolledpanel as scrolled

class MyFrame(wx.Frame):
    def __init__(self, parent=None):
        super(MyFrame, self).__init__(parent, title="Trive", size=wx.DisplaySize())
        # create main panel - to put on the others panels
        main_panel = MainPanel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(main_panel, 1, wx.EXPAND)

        # arrange the frame
        self.SetSizer(box)
        self.Layout()
        self.Show()
        self.Maximize()

class MainPanel(wx.Panel):
    '''
    class that create the main layout
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.frame = parent
        self.SetBackgroundColour(wx.BLACK)
        self.v_box = wx.BoxSizer()

        # create object for each panel
        self.login = LoginPanel(self, self.frame)
        self.registration = RegisterPanel(self, self.frame)
        self.loby = FilesPanel(self,self.frame)
#        self.account = AccountPanel(self, self.frame)

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

        # create a new panel
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, size=wx.DisplaySize(), style=wx.SIMPLE_BORDER)
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
        self.font = wx.Font(22, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        #create sizer for the username
        nameBox = wx.BoxSizer(wx.HORIZONTAL)

        self.create_userName_field()

        # add the user logo
        user = wx.Image('draws\\user.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        user_logo = wx.StaticBitmap(self, -1, user, (565, 275), (user.GetWidth(), user.GetHeight()))

        #update the username sizer
        nameBox.Add(user_logo, 0, wx.ALL, 0)
        nameBox.Add(self.userNameField, 0, wx.ALL, 5)

        #create sizer for the password
        passBox = wx.BoxSizer(wx.HORIZONTAL)

        self.create_password_field()

        # add the fingerprint logo
        finger = wx.Image('draws\\finger.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        finger_logo = wx.StaticBitmap(self, -1, finger, (565, 383), (finger.GetWidth(), finger.GetHeight()))

        #update the password sizer
        passBox.Add(finger_logo, 0, wx.ALL, 0)
        passBox.Add(self.passWordField, 0, wx.ALL, 5)

        lobyBtn = wx.Button(self, wx.ID_ANY, label="loby", size=(400, 40))   #backdoor
        lobyBtn.Font = self.font.Bold()
        lobyBtn.BackgroundColour = wx.BLACK
        lobyBtn.ForegroundColour = wx.GREEN
        lobyBtn.Bind(wx.EVT_BUTTON, self.handle_loby)

        # add all elements to sizer
        self.sizer.Add(trive,0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(100)
        self.sizer.Add(nameBox,0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(passBox,0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(20)
        self.add_buttons()

        # arrange the screen
        self.SetSizer(self.sizer)
        self.Layout()
        self.Hide()

    def errorMsg(self, msg):
        '''

        :param msg:massage to shoe in the error
        :return: create and shoe the error massage
        '''
        wx.MessageBox(msg, 'Trive Error', wx.OK | wx.ICON_HAND )

    def add_buttons(self):
        '''

        :return: add all the buttons
        '''

        self.createBtn('Login', self.handle_login, (400, 40))

        self.createBtn('Not a member? sign up!', self.handle_reg, (400, 40))

        # size down the font for the forgot your password button
        self.font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        self.createBtn('forgot your password?', self.handle_forgot_password, (250, 30))

    def createBtn(self, msg, func, size):
        '''

        :param msg: the msg to put in the button
        :param func: function to bind to the button
        :return:
        '''
        # create the button
        Btn = wx.Button(self, wx.ID_ANY, label=msg, size=size)
        # design the button
        if msg == 'Login':
            Btn.Font = self.font.Bold()
        elif msg == 'forgot your password?':
            Btn.Font = self.font.MakeUnderlined()
        else:
            Btn.Font = self.font
        Btn.BackgroundColour = wx.BLACK
        Btn.ForegroundColour = wx.GREEN
        Btn.Bind(wx.EVT_BUTTON, func)
        self.sizer.Add(Btn, 0, wx.CENTER | wx.ALL, 5)

    def create_userName_field(self):
        '''

        :return:create and design the userName textField
        '''
        #create the tet field
        self.userNameField = wx.TextCtrl(self, 10, name="username", style=wx.TEXT_ATTR_BULLET_STYLE_ROMAN_UPPER, size=(500, 38))

        # design the username text field
        self.userNameField.SetHint('username:')
        self.userNameField.SetBackgroundColour(wx.BLACK)
        self.userNameField.SetForegroundColour(wx.WHITE)
        self.userNameField.Font = self.font

    def create_password_field(self):
        '''

        :return:create and design the password textField
        '''
        # create the password text field
        self.passWordField = wx.TextCtrl(self, -1, name="password", style=wx.TE_PASSWORD, size=(500, 38))

        # design the password text field
        self.passWordField.SetHint('password:')
        self.passWordField.SetBackgroundColour(wx.BLACK)
        self.passWordField.SetForegroundColour(wx.WHITE)
        self.passWordField.SetFont(self.font)

    def handle_login(self, event):
        '''

        :param event:event that happend on the screen
        :return:take care the event when pressing login button
        '''
        username = self.userNameField.GetValue()
        password = self.passWordField.GetValue()

        if not username or not password :
            self.errorMsg('You must enter username and password!')
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

    def handle_loby(self, event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        self.Hide()
        self.parent.loby.Show()

class RegisterPanel(wx.Panel):
    '''
        class that create the register layout
    '''

    def __init__(self, parent, frame):

        # create a new panel
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, size=wx.DisplaySize(), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        self.__create_screen__()

    def __create_screen__(self):
        self.Hide()
        # create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        # add the Trive logo
        png = wx.Image('draws\\logo.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        logo = wx.StaticBitmap(self, -1, png, (650, -2), (png.GetWidth(), png.GetHeight()))

        # font for the text
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        # create sizer for the email
        emailBox = wx.BoxSizer(wx.HORIZONTAL)

        self.create_email_field()

        # add the email logo
        email = wx.Image('draws\\email.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        email_logo = wx.StaticBitmap(self, -1, email, (565, 275), (email.GetWidth(), email.GetHeight()))

        #update the email sizer
        emailBox.Add(email_logo, 0, wx.ALL, 0)
        emailBox.Add(self.emailField, 0, wx.ALL, 0)

        # create sizer for the username
        nameBox = wx.BoxSizer(wx.HORIZONTAL)

        self.create_userName_field()

        # add the user logo
        user = wx.Image('draws\\user.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        user_logo = wx.StaticBitmap(self, -1, user, (565, 275), (user.GetWidth(), user.GetHeight()))

        # update the username sizer
        nameBox.Add(user_logo, 0, wx.ALL, 0)
        nameBox.Add(self.userNameField, 0, wx.ALL, 5)

        # create sizer for the password
        passBox = wx.BoxSizer(wx.HORIZONTAL)

        self.create_password_field()

        # add the fingerprint logo
        finger = wx.Image('draws\\finger.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        finger_logo = wx.StaticBitmap(self, -1, finger, (565, 383), (finger.GetWidth(), finger.GetHeight()))

        #update the password sizer
        passBox.Add(finger_logo, 0, wx.ALL, 0)
        passBox.Add(self.passWordField, 0, wx.ALL, 5)

        self.sizer.Add(logo, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(100)
        self.sizer.Add(emailBox, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(nameBox, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(passBox, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(20)
        self.add_buttons()

        # arrange the screen
        self.SetSizer(self.sizer)
        self.Layout()
        self.Hide()

    def errorMsg(self, msg):
        '''

        :param msg:massage to shoe in the error
        :return: create and shoe the error massage
        '''
        wx.MessageBox(msg, 'Trive Error', wx.OK | wx.ICON_HAND )

    def add_buttons(self):
        '''

        :return: add all the buttons
        '''

        self.createBtn('Register', self.handle_reg, (400, 40))

        self.createBtn('Login', self.handle_login, (400, 40))

    def createBtn(self, msg, func, size):
        '''

        :param msg: the msg to put in the button
        :param func: function to bind to the button
        :return:
        '''
        # create the button
        Btn = wx.Button(self, wx.ID_ANY, label=msg, size=size)
        # design the button
        if msg == 'Register':
            Btn.Font = self.font.Bold()
        else:
            Btn.Font = self.font
        Btn.BackgroundColour = wx.BLACK
        Btn.ForegroundColour = wx.GREEN
        Btn.Bind(wx.EVT_BUTTON, func)
        self.sizer.Add(Btn, 0, wx.CENTER | wx.ALL, 5)

    def create_userName_field(self):
        '''

        :return:create and design the userName textField
        '''
        #create the tet field
        self.userNameField = wx.TextCtrl(self, 10, name="username", style=wx.TEXT_ATTR_BULLET_STYLE_ROMAN_UPPER, size=(500, 38))

        # design the username text field
        self.userNameField.SetHint('username:')
        self.userNameField.SetBackgroundColour(wx.BLACK)
        self.userNameField.SetForegroundColour(wx.WHITE)
        self.userNameField.Font = self.font

    def create_password_field(self):
        '''

        :return:create and design the password textField
        '''
        # create the password text field
        self.passWordField = wx.TextCtrl(self, -1, name="password", style=wx.TE_PASSWORD, size=(500, 38))

        # design the password text field
        self.passWordField.SetHint('password:')
        self.passWordField.SetBackgroundColour(wx.BLACK)
        self.passWordField.SetForegroundColour(wx.WHITE)
        self.passWordField.SetFont(self.font)

    def create_email_field(self):
        '''

        :return:create and design the email textField
        '''
        # create the email text field
        self.emailField = wx.TextCtrl(self, -1, name="email", size=(500, 38))

        # design the email text field
        self.emailField.SetFont(self.font)
        self.emailField.SetHint('email:')
        self.emailField.SetBackgroundColour(wx.BLACK)
        self.emailField.SetForegroundColour(wx.WHITE)

    def handle_reg(self, event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        # mean someone create account
        username = self.userNameField.GetValue()
        password = self.passWordField.GetValue()
        email = self.emailField.GetValue()

        if not username or not password or not email:
            self.errorMsg('You must enter username, password and email')
        else:
            pass
            # self.frame.SetStatusText("waiting for Server approve")

    def handle_login(self, event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        self.Hide()
        self.parent.login.Show()

class FilesPanel(wx.Panel):

    def __init__(self, parent, frame):
        # create a new panel
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, size=wx.DisplaySize(), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        self.files = ['a.txt1','fdjgdsf', 'tamirr', 'tamirr','tamirr','tamirr','fdjgdsf', 'tamirr', 'tamirr','tamirr','tamirr','fdjgdsf', 'tamirr', 'tamirr','tamirr','tamirr', 'fdjgdsf', 'tamirr', 'tamirr','tamirr','tamirr', 'tamirr', 'tamirr','tamirr','tamirr', 'tamirr', 'tamirr','tamirr','tamirr', 'tamirr', 'tamirr','tamirr','tamirr']#,'tamirr','tamirr','tamirr']
        self.__create_screen__()

    def __create_screen__(self):
        self.Hide()
        # create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        # add the Trive logo
        png = wx.Image('draws\\logo.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        logo = wx.StaticBitmap(self, -1, png, (650, -2), (png.GetWidth(), png.GetHeight()))

        # font for the text
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        self.createFilesSizer()
        self.addOptins()

        self.sizer.Add(logo, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(20)
        self.sizer.Add(self.scrollP, 0, wx.CENTER | wx.ALL)
        self.sizer.AddSpacer(20)
        self.sizer.Add(self.optionsSizer, 0, wx.CENTER | wx.ALL)

        # arrange the screen
        self.SetSizer(self.sizer)
        self.Layout()
        self.Hide()

    def createFilesSizer(self):
        '''

        :return: show in the screen the files that are on top of the directories
        '''

        self.scrollP = scrolled.ScrolledPanel(self, -1, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER,size=(wx.DisplaySize()[0] - 200, wx.DisplaySize()[1] - 350))


        placeFilesSizer = wx.BoxSizer(wx.VERTICAL)
        self.filesSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.filesSizer.AddSpacer(200)
        itemsInsizerCount = 0
        placeFilesSizer.AddSpacer(220)

        for file in self.files:
            if itemsInsizerCount > 8:
                placeFilesSizer.AddSpacer(10)
                placeFilesSizer.Add(self.filesSizer)
                self.filesSizer = wx.BoxSizer(wx.HORIZONTAL)
                self.filesSizer.AddSpacer(200)
                itemsInsizerCount = 0
                placeFilesSizer.AddSpacer(50)

            self.filesSizer.AddSpacer(45)
            self.filesSizer.Add(self.createFileSizer(file), 0, flag=wx.ALIGN_CENTER | wx.ALL)
            itemsInsizerCount += 1

        placeFilesSizer.Add(self.filesSizer)
        self.scrollP.SetSizer(placeFilesSizer)
        self.scrollP.SetupScrolling()

    def createFileSizer(self, file):
        '''

        :return: create sizer for file(file image, file name)
        '''

        fileSizer = wx.BoxSizer(wx.VERTICAL)

        # add the file logo
        img = wx.Image('draws\\file.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        fileImg = wx.StaticBitmap(self, -1, img, (650, -2), (img.GetWidth(), img.GetHeight()))
        fileSizer.Add(fileImg, 0, wx.CENTER | wx.ALL)

        file_name = wx.StaticText(self, -1, label=file)
        file_name.SetForegroundColour(wx.GREEN)
        file_name.SetFont(self.font)

        fileSizer.Add(file_name, 0, wx.CENTER | wx.ALL)

        return fileSizer


    def addOptins(self):
        '''

        :return: add all the optins in the buttom to sizer
        '''
        self.optionsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.optionsSizer.AddSpacer(80)

        # create the add folder button
        self.createBtn(self.optionsSizer, "Account", self.handle_account)

        # create the upload button
        self.createBtn(self.optionsSizer, "Upload file", self.handle_upload)

        # create the add folder button
        self.createBtn(self.optionsSizer, "Create folder", self.handle_createFolder)

    def createBtn(self, sizer, msg, func):
        '''

        :param sizer: sizer to put the Btn in
        :param msg: the msg to put in the button
        :param func: function to bind to the button
        :return:
        '''
        # create the button
        Btn = wx.Button(self, wx.ID_ANY, label=msg, size=(250, 40))
        # design the button
        Btn.Font = self.font
        Btn.BackgroundColour = wx.BLACK
        Btn.ForegroundColour = wx.GREEN
        Btn.Bind(wx.EVT_BUTTON, func)
        sizer.Add(Btn)
        sizer.AddSpacer(50)

    def handle_upload(self, event):
        '''

        :param event:  means  the upload btn pressed
        :return:
        '''
        openFileDialog = wx.FileDialog(self, "Open", "", "", "",wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        openFileDialog.Destroy()
        print(path)
        if self.getType(path.split('\\')[-1]) == 'no':
            self.errorMsg('Trive doesnt support this type of files')

    def getType(self, fileName):
        '''

        :param fileName: name of file
        :return:  "img" if the file is some image, "file" if the file is some text file, "folder" if the fileName if folder, "no"
        '''
        if not '.' in fileName:     #mean that the filename if folder
            return 'folder'
        else:
            typ = fileName.split('.')[1]
            if typ == 'jpg' or typ == 'bmp' or typ == 'png' or typ == 'svg':
                return 'img'
            elif typ == 'txt' or typ == 'py' or typ == 'java' or typ == 'word' or typ == 'bin' or typ == 'doc' or typ == 'docx' or typ == 'asm':
                return 'file'
            else:
                return 'no'

    def handle_createFolder(self, event):
        '''

        :param event:  means  the upload file btn pressed
        :return:
        '''
        pass

    def handle_account(self, event):
        '''

        :param event:  means the upload btn pressed
        :return:
        '''
        #self.parent.account.Show()
        pass

    def errorMsg(self, msg):
        '''

        :param msg:massage to shoe in the error
        :return: create and shoe the error massage
        '''
        wx.MessageBox(msg, 'Trive Error', wx.OK | wx.ICON_HAND )

'''class AccountPanel(wx.Panel):

    def __init__(self, parent, frame):
        # create a new panel
        wx.Panel.__init__(self, parent, size=(400, wx.DisplaySize()[1]), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        self.Hide()
        self.__create_screen__()

    def __create_screen__(self):

        # create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        # add the Trive logo
        png = wx.Image('draws\\logo.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        logo = wx.StaticBitmap(self, -1, png, (650, -2), (png.GetWidth(), png.GetHeight()))

        # font for the text
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)
'''




if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()