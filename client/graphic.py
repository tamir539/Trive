import wx
import wx.lib.scrolledpanel as scrolled
from pubsub import pub
import queue


class MyFrame(wx.Frame):
    def __init__(self, q, parent=None):
        super(MyFrame, self).__init__(parent, title="Trive", size=wx.DisplaySize())
        # create main panel - to put on the others panels
        main_panel = MainPanel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(main_panel, 1, wx.EXPAND)
        self.q = q

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
        self.loby = LobyPanel(self,self.frame)

        #self.account = AccountPanel(self, self.frame)

        self.v_box.Add(self.login)

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
        self.trys = 0
        self.__create_screen__()

    def __create_screen__(self):
        # create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        #add the Trive logo
        png = wx.Image('draws\\logo.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        trive = wx.StaticBitmap(self, -1, png, (650, -2), (png.GetWidth(), png.GetHeight()))

        self.flag = 'login'

        pub.subscribe(self.handle_answer, self.flag)  # talk with the logic client

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
            self.username = username
            self.frame.q.put((self.flag, [username, password]))

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
        dlg = wx.TextEntryDialog(None, 'Enter username: ','get 1 time password to your email', '',style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            email = dlg.GetValue()
            self.frame.q.put(('forgot_password', [email]))

    def handle_loby(self, event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        self.Hide()
        self.parent.loby.Show()

    def handle_answer(self, answer):
        '''

        :param answer: answer from the server
        :return: if answer is "ok" go to the lobby, otherwise error msg
        '''
        if answer == 'no':
            self.errorMsg('Wrong username or password')
        elif answer =='ok':
            #move to loby
            self.Hide()
            self.parent.loby.Show()
        else:
            self.errorMsg('This ip has been blocked!')
            self.frame.Destroy()


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

        self.flag = 'register'

        pub.subscribe(self.handle_answer, self.flag)    #talk with the logic client

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
            self.email = email
            self.username = username
            self.frame.q.put((self.flag ,[email, username, password]))

    def handle_login(self, event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        self.Hide()
        self.parent.login.Show()

    def handle_answer(self, answer):
        if answer == 'un':
            self.errorMsg('This username is already taken')
        else:
            wx.MessageBox(f'Welcome {self.username}!', 'Trive', wx.OK | wx.ICON_NONE)
            self.Hide()
            self.parent.login.Show()


class LobyPanel(wx.Panel):

    def __init__(self, parent, frame):
        # create a new panel
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, size=wx.DisplaySize(), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        self.inAccount = False
        self.account = None
        self.scrollFiles = None

        self.new_folder_name = ''
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

        #create the files scroller
        self.scrollFiles = ScrollFilesPanel(self, self.parent.frame)

        # create the files scroller
        self.account = AccountPanel(self, self.parent.frame)

        #add the options
        self.addOptins()

        self.sizer.Add(logo, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(wx.DisplaySize()[1] - png.GetHeight() - 140)
        self.sizer.Add(self.optionsSizer, 0, wx.CENTER | wx.ALL)

        # arrange the screen
        self.SetSizer(self.sizer)
        self.Layout()

    def addOptins(self):
        '''

        :return: add all the optins in the buttom to sizer
        '''
        self.optionsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.optionsSizer.AddSpacer(80)

        # create the upload button
        self.accountOrFiles = self.createBtn(self.optionsSizer, "Account", self.handle_account)

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
        return Btn

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
        else:
            self.frame.q.put(('upload', [path]))

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
        dlg = wx.TextEntryDialog(None, 'Enter name for the folder: ', 'Create folder', '',style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            self.new_folder_name = dlg.GetValue()
            path = self.scrollFiles.path + '\\' + self.new_folder_name   #calculate the virtual path
            self.frame.q.put(('create_folder', [path]))
            pub.subscribe(self.handle_create_folder_answer, 'create_folder')

    def handle_account(self, event):
        '''

        :param event:  means the upload btn pressed
        :return:
        '''
        if self.inAccount:
            self.account.Hide()
            self.scrollFiles.Show()
            self.accountOrFiles.SetLabel('Account')
        else:
            self.account.Show()
            self.scrollFiles.Hide()
            self.accountOrFiles.SetLabel('Files')

        self.inAccount = not self.inAccount

        pass

    def handle_create_folder_answer(self, answer):
        '''

        :param answer:answer from the server
        :return:
        '''
        if answer == 'ok':
            wx.MessageBox(f'Folder {self.new_folder_name} created successfuly!', 'Trive', wx.OK | wx.ICON_INFORMATION)
            self.scrollFiles.add_file(self.new_folder_name)
            self.new_folder_name = ''
        else:
            wx.MessageBox(f'There was an error in creating {self.new_folder_name} folder', 'Trive Error', wx.OK | wx.ICON_ERROR)

    def errorMsg(self, msg):
        '''

        :param msg:massage to shoe in the error
        :return: create and shoe the error massage
        '''
        wx.MessageBox(msg, 'Trive Error', wx.OK | wx.ICON_HAND )


class ScrollFilesPanel(scrolled.ScrolledPanel):
    '''
        class that show all the top level files on the screen
    '''
    def __init__(self, parent, frame):

        panelDepth = wx.DisplaySize()[0] - 300
        panelLength = wx.DisplaySize()[1] - 350

        screenLength = wx.DisplaySize()[1]
        screenDepth = wx.DisplaySize()[0]

        # create a new panel
        scrolled.ScrolledPanel.__init__(self, parent,pos =((screenDepth - panelDepth)/2, 200), size=(panelDepth, panelLength ), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        self.files = ['blocked_ips.txt','folder1', 'a.py', 'cat.jpg']

        pub.subscribe(self.download_ans, 'finish_download')

        self.path = ''      #the virtual path we are in

        self.__create_screen__()

    def __create_screen__(self):
        self.Hide()

        # change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        # font for the text
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        self.createFilesSizer()

        self.Show()

    def createFilesSizer(self):
        '''

        :return: show in the screen the files that are on top of the directories
        '''

        placeFilesSizer = wx.BoxSizer(wx.VERTICAL)
        self.filesSizer = wx.BoxSizer(wx.HORIZONTAL)

        itemsInsizerCount = 0

        for file in self.files:
            if itemsInsizerCount > 9:   #check that there are not more then 10 files in a row
                placeFilesSizer.Add(self.filesSizer)
                self.filesSizer = wx.BoxSizer(wx.HORIZONTAL)
                placeFilesSizer.AddSpacer(50)
                itemsInsizerCount = 0

            self.filesSizer.AddSpacer(45)
            self.filesSizer.Add(self.createFileSizer(file), 0, flag=wx.ALIGN_CENTER | wx.ALL)
            itemsInsizerCount += 1

        placeFilesSizer.Add(self.filesSizer)
        self.SetSizer(placeFilesSizer)
        self.SetupScrolling()

    def createFileSizer(self, file):
        '''
        @:param file: name of the file
        :return: create sizer for file(file image, file name)
        '''

        fileSizer = wx.BoxSizer(wx.VERTICAL)

        # add the file\image\folder logo
        img = wx.Image(f'draws\\{self.getType(file)}.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        fileImg = wx.StaticBitmap(self, -1, img, (650, -2), (img.GetWidth(), img.GetHeight()))
        fileImg.SetName(file)
        fileImg.Bind(wx.EVT_RIGHT_DOWN, self.onFileClick)
        fileSizer.Add(fileImg, 0, wx.CENTER | wx.ALL)

        if self.getType(file) == 'folder':
            fileImg.Bind(wx.EVT_LEFT_DCLICK, self.get_into_folder)

        #add the name of the file\image\folder
        file_name = wx.StaticText(self, -1, label=file)
        file_name.SetForegroundColour(wx.WHITE)
        file_name.SetFont(self.font)

        fileSizer.Add(file_name, 0, wx.CENTER | wx.ALL)

        return fileSizer

    def getType(self, fileName):
        '''

        :param fileName: name of file
        :return:  "image" if the file is some image, "file" if the file is some text file, "folder" if the fileName if folder, "no"
        '''
        if not '.' in fileName:     #mean that the filename if folder
            return 'folder'
        else:
            typ = fileName.split('.')[1]
            if typ == 'jpg' or typ == 'bmp' or typ == 'png' or typ == 'svg':
                return 'image'
            elif typ == 'txt' or typ == 'py' or typ == 'java' or typ == 'word' or typ == 'bin' or typ == 'doc' or typ == 'docx' or typ == 'asm':
                return 'file'
            else:
                return 'no'

    def onFileClick(self, event):
        '''

        :param event:event mean that file pressed
        :return:change the current pressed file of the class
        '''
        widget = event.GetEventObject()
        fileName = widget.GetName()
        self.PopupMenu(OptionsMenu(self, self.getType(fileName),fileName, self.path))

    def get_into_folder(self, event):
        widget = event.GetEventObject()
        folder_name = widget.GetName()
        self.path += '\\' + folder_name
        print('in path ', self.path)

    def download_ans(self, ans):
        if ans == 'ok':
            wx.MessageBox('downloaded successfully', 'Trive', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Downloaded error', 'Trive error', wx.OK | wx.ICON_ERROR)

    def add_file(self, file_name):
        '''

        :param file_name:
        :return:
        '''
        self.files.append(file_name)
        self.createFilesSizer()
        # file_sizer = self.createFileSizer(file_name)
        # self.filesSizer.AddSpacer(45)
        # self.filesSizer.Add(file_sizer, 0, flag=wx.ALIGN_CENTER | wx.ALL)

class AccountPanel(wx.Panel):

    def __init__(self, parent, frame):
        panelDepth = wx.DisplaySize()[0] - 300
        panelLength = wx.DisplaySize()[1] - 350

        screenLength = wx.DisplaySize()[1]
        screenDepth = wx.DisplaySize()[0]

        # create a new panel
        wx.Panel.__init__(self, parent,pos =((screenDepth - panelDepth)//2, 200), size=(panelDepth, panelLength ), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent

        self.__create_screen__()

    def __create_screen__(self):
        self.Hide()
        # create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        # font for the text
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        #add the account logo
        user = wx.Image('draws\\userForLoby.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        user_img = wx.StaticBitmap(self, -1 ,user,  pos = (wx.DisplaySize()[0] - wx.DisplaySize()[0]//7, 30), size = (user.GetWidth(), user.GetHeight()))

        try_email = 'Email: tamir.burstein@gmail.com'
        try_username = 'Username: tamir539'

        self.addOptins()

        #create the email text
        email = wx.StaticText(self, -1, label=try_email)
        email.SetForegroundColour(wx.WHITE)
        email.SetFont(self.font)

        # create the username text
        username = wx.StaticText(self, -1, label=try_username)
        username.SetForegroundColour(wx.WHITE)
        username.SetFont(self.font)

        self.sizer.Add(user_img,0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(email,0,wx.ALL, 5)
        self.sizer.Add(username, 0, wx.ALL, 5)
        self.sizer.AddSpacer(100)
        self.sizer.Add(self.optionsSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # arrange the screen
        self.SetSizer(self.sizer)
        self.Layout()

    def addOptins(self):
        '''

        :return: add all the optins in the buttom to sizer
        '''
        self.optionsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.optionsSizer.AddSpacer(80)

        # create the change password button
        self.createBtn(self.optionsSizer, "Change password", self.handle_changePassword)

        # create the change email button
        self.createBtn(self.optionsSizer, "Change email", self.handle_change_email)

        # create the logout email button
        self.createBtn(self.optionsSizer, "Logout", self.handle_logOut)

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

    def handle_changePassword(self, event):
        '''

        :param event:change password pressed
        :return: get the new password and notify the logic
        '''
        dlg = wx.TextEntryDialog(None, 'Enter new Password: ', 'Change Password', '',style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            new_password = dlg.GetValue()
            self.frame.q.put(('change_detail', [f'password:{new_password}']))

    def handle_change_email(self, event):
        '''

        :param event:change email pressed
        :return: get the new email and notify the logic
        '''
        dlg = wx.TextEntryDialog(None, 'Enter new Email: ', 'Change Email', '', style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            new_email = dlg.GetValue()
            self.frame.q.put(('change_detail', [f'email:{new_email}']))

    def handle_logOut(self, event):
        pass


class OptionsMenu(wx.Menu):

    def __init__(self, parent, file_typ, file_name, path):
        super(OptionsMenu, self).__init__()

        self.parent = parent
        self.file_name = file_name
        self.file_typ = file_typ
        self.path = path
        self.createOptions()

    def createOptions(self):
        '''

        :return: create all the options
        '''
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        self.Bind(wx.EVT_MENU, self.getChosen)
        if self.file_typ == 'file':
            self.commandById = {1: 'Download', 2: 'Rename', 3: 'Share', 4: 'Add to folder', 5: 'Edit' ,6: 'Delete'}
            self.funcById = {1: self.download, 2: self.rename, 3: self.share, 4:self.addToFolder, 5:self.edit, 6: self.delete}  #button id -> function that handle if the button selected
        else:
            self.commandById = {1: 'Download', 2: 'Rename', 3: 'Share', 4: 'Add to folder', 6: 'Delete'}
            self.funcById = {1: self.download, 2: self.rename, 3: self.share, 4: self.addToFolder, 6: self.delete}

        for id in self.commandById.keys():
            self.createOption(id)

    def createOption(self, id):
        '''

        :param id: id for the option
        :return: creates the option and add to the menu
        '''
        popmenu = wx.MenuItem(self, id, self.commandById[id])
        popmenu.SetBackgroundColour(wx.BLACK)
        popmenu.SetTextColour(wx.WHITE)
        popmenu.SetFont(self.font)
        self.Append(popmenu)

    def getChosen(self, event):
        '''

        :param event:
        :return: return the id of the selected command
        '''
        id = event.GetId()
        self.funcById[id]()

    def download(self):
        self.parent.frame.q.put(('download', [self.path + '\\' + self.file_name]))

    def rename(self):

        dlg = wx.TextEntryDialog(None, f'Enter new name for the {self.file_typ}: ', f'Rename {self.file_typ}', '',style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            self.parent.frame.q.put(('rename', [self.path + '\\' + self.file_name, name]))

    def share(self):

        dlg = wx.TextEntryDialog(None, f'Enter username to share with: ', f'Share {self.file_typ}', '',style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            username = dlg.GetValue()
            self.parent.frame.q.put(('share', [self.path + '\\' + self.file_name, username]))
            wx.MessageBox(f'If the username exists, he will get the {self.file_typ}', 'Trive', wx.OK)

    def addToFolder(self):
        print('add to folder')

    def delete(self):
        question = wx.MessageBox('Are you sure you want to delete this file? ', 'Trive Error', wx.YES | wx.NO | wx.ICON_WARNING)
        if question == wx.YES:
            self.parent.frame.q.put(('delete', [self.path + '\\' + self.file_name]))

    def edit(self):
        print('edit')


if __name__ == '__main__':
    q = queue.Queue()
    app = wx.App()
    frame = MyFrame(q)
    app.MainLoop()