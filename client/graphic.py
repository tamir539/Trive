import wx
import wx.lib.scrolledpanel as scrolled
from pubsub import pub
import queue
import re


class MyFrame(wx.Frame):
    def __init__(self, q, parent=None):

        super(MyFrame, self).__init__(parent, title="Trive", size=wx.DisplaySize())
        self.username = ''
        self.email = ''
        self.status_bar = self.CreateStatusBar(1)
        self.status_bar.SetBackgroundColour(wx.BLACK)

        # create main panel - to put on the others panels
        main_panel = MainPanel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(main_panel, 1, wx.EXPAND)
        self.q = q

        # loc = wx.IconLocation('draws\\logo.jpg', wx.BITMAP_TYPE_ICO)
        # self.SetIcon(loc)

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
        self.username = ''
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
        dlg = wx.TextEntryDialog(None, 'Enter username: ','get new password to your email', '',style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            email = dlg.GetValue()
            self.frame.q.put(('forgot_password', [email]))
            wx.MessageBox('If the username exists, he will get the email')

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

        ans = answer.split(',')[0]
        if ans == 'no':
            self.errorMsg('Wrong username or password')
        elif ans == 'ac':
            self.errorMsg('You already connected from other device!')
        elif ans =='ok':
            email = answer.split(',')[1]
            self.frame.username = self.username
            self.frame.email = email
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

        #check email input
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        result = re.match(pattern, email)

        if not username or not password or not email:
            self.errorMsg('You must enter username, password and email')
        elif not result:
            wx.MessageBox('Invalid Email', 'Trive Error', wx.OK | wx.ICON_ERROR)
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
        self.uploading = False      #'true' - > upload in progress
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

        pub.subscribe(self.uplod_answer, 'upload')

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

        # create the paste button
        self.createBtn(self.optionsSizer, "Paste here", self.handle_paste)

        # create the account button
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
        if 'recycle' in self.scrollFiles.path or 'shared' in self.scrollFiles.path:
            self.errorMsg('Cant upload here')
        else:
            openFileDialog = wx.FileDialog(self, "Open", "", "", "",wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            openFileDialog.ShowModal()
            #path of the selected file
            path = openFileDialog.GetPath()
            if path != '':
                file_name = path[path.rindex('\\') + 1:]
                openFileDialog.Destroy()
                if self.uploading:
                    self.errorMsg('Wait the other upload to finish!')
                elif self.getType(path.split('\\')[-1]) == 'no':
                    self.errorMsg('Trive doesnt support this type of files')
                #check that the file isnt allready exists
                elif file_name in self.scrollFiles.files[self.scrollFiles.path]:
                    self.errorMsg('File allready exists')
                else:
                    self.frame.status_bar.SetBackgroundColour(wx.WHITE)
                    self.frame.status_bar.SetStatusText(f'Uploading {file_name}')
                    self.frame.q.put(('upload', [path, self.scrollFiles.path]))
                    self.uploading = True

    def getType(self, fileName):
        '''

        :param fileName: name of file
        :return:  "img" if the file is some image, "file" if the file is some text file, "folder" if the fileName if folder, "no"
        '''

        files = ['txt', 'py', 'java', 'word', 'bin', 'docx', 'doc', 'asm', 'pptx', 'xlxs']
        images = ['jpg', 'bmp', 'png', 'svg']

        if not '.' in fileName:     #mean that the filename if folder
            return 'folder'
        else:
            typ = fileName.split('.')[1]
            if typ in images:
                return 'img'
            elif typ in files:
                return 'file'
            else:
                return 'no'

    def handle_createFolder(self, event):
        '''

        :param event:  means  the upload file btn pressed
        :return:
        '''
        if 'recycle' in self.scrollFiles.path or 'shared' in self.scrollFiles.path:
            wx.MessageBox('Cant create folder here', 'Trive error', wx.OK | wx.ICON_ERROR)
        else:
            dlg = wx.TextEntryDialog(None, 'Enter name for the folder: ', 'Create folder', '',style=wx.TextEntryDialogStyle)

            if dlg.ShowModal() == wx.ID_OK:
                self.new_folder_name = dlg.GetValue()
                if self.new_folder_name == 'shared':
                    wx.MessageBox('Unavailabale name', 'Trive Error', wx.OK | wx.ICON_ERROR)
                else:
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
            #set the username and email of the user
            self.account.username.SetLabel(f'Username: {self.frame.username}')
            self.account.email.SetLabel(f'Email: {self.frame.email}')
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

    def uplod_answer(self, answer):
        '''

        :param answer:answer from the server from the upload
        :return: show the answer for the server
        '''
        self.frame.status_bar.SetBackgroundColour(wx.BLACK)
        self.frame.status_bar.SetStatusText('')
        ans = answer.split(',')[0]
        file_name = answer.split(',')[1]
        if ans == 'ok':
            wx.MessageBox(f'{file_name} uploaded successfully', 'Trive',wx.OK | wx.ICON_INFORMATION)
            self.scrollFiles.add_file(file_name)
        else:
            wx.MessageBox(f'There was an error in uploading {file_name}', 'Trive Error',wx.OK | wx.ICON_ERROR)
        self.uploading = False

    def handle_paste(self, event):
        '''

        :param event:
        :return: paste the last copyed file in this path
        '''
        copyied = self.scrollFiles.copying
        if copyied == '':
            self.errorMsg('No file or folder has been selected')
        elif 'recycle' in self.scrollFiles.path or 'shared' in self.scrollFiles.path:
            self.errorMsg('Cant paste here')
        else:
            self.frame.q.put(('add_to_folder', [copyied, self.scrollFiles.path]))
            pub.subscribe(self.add_to_folder_answer, 'add_to_folder')

    def add_to_folder_answer(self, answer):
        '''

        :param answer:answer from the server
        :return:show the answer to the client
        '''

        if answer == 'ok':
            copyied = self.scrollFiles.copying
            copyied_name = copyied[copyied.rindex('\\') + 1:]
            delete_from_path = copyied[:copyied.rindex('\\')]
            #add the file to the selected folder
            self.scrollFiles.add_file(copyied_name)


class ScrollFilesPanel(scrolled.ScrolledPanel):
    '''
        class that show all the top level files on the screen
    '''
    def __init__(self, parent, frame):

        panelDepth = wx.DisplaySize()[0] - 300
        panelLength = wx.DisplaySize()[1] - 350

        screenDepth = wx.DisplaySize()[0]

        # create a new panel
        scrolled.ScrolledPanel.__init__(self, parent,pos =((screenDepth - panelDepth)/2, 200), size=(panelDepth, panelLength ), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        self.files = {}     #folder path -> all the files in this path
        self.got_files = False
        self.path = ''      #the virtual path we are in
        self.copying = ''       #the virtual path for the file that now in copy
        self.__create_screen__()

    def __create_screen__(self):
        self.Hide()

        # change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        # font for the text
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)
        # while not self.got_files:
        #     pass

        pub.subscribe(self.download_ans, 'finish_download')
        pub.subscribe(self.get_files, 'get_all_files')
        pub.subscribe(self.rename_ans, 'rename')
        pub.subscribe(self.delete_ans, 'delete')
        pub.subscribe(self.share_ans, 'share')
        #self.get_files(r'T:\public\aaaaTamir\client,draws,x,graphic.py,T:\public\aaaaTamir\client\draws,email.jpg,file.png,finger.jpg,logo.jpg,temp1.py,user.jpg,T:\public\aaaaTamir\client\x,tam.txt')

        self.Show()

    def createFilesSizer(self, files):
        '''

        :param index: index in self.files dictionary
        :return: show in the screen the files that are on top of the directories
        '''

        self.placeFilesSizer = wx.BoxSizer(wx.VERTICAL)
        self.filesSizer = wx.BoxSizer(wx.HORIZONTAL)

        itemsInsizerCount = 0
        char_count = 0
        self.placeFilesSizer.AddSpacer(20)

        for file in files:
            if char_count + len(file) > 70 or itemsInsizerCount > 6:   #check that there are not more then 10 files in a row
                self.placeFilesSizer.Add(self.filesSizer)
                self.filesSizer = wx.BoxSizer(wx.HORIZONTAL)
                self.placeFilesSizer.AddSpacer(50)
                itemsInsizerCount = 0
                char_count = 0

            self.filesSizer.AddSpacer(45)
            self.filesSizer.Add(self.createFileSizer(file), 0, flag=wx.ALIGN_CENTER | wx.ALL)
            itemsInsizerCount += 1
            char_count += len(file)

        self.placeFilesSizer.Add(self.filesSizer)
        self.SetSizer(self.placeFilesSizer)
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

        fileSizer.Add(fileImg, 0, wx.CENTER | wx.ALL)

        if self.getType(file) == 'folder':
            fileImg.Bind(wx.EVT_LEFT_DCLICK, self.get_into_folder)

        if self.getType(file) == 'back':
            fileImg.Bind(wx.EVT_LEFT_DOWN, self.handle_back)

        elif file != 'shared' and file != 'recycle':
            fileImg.Bind(wx.EVT_RIGHT_DOWN, self.onFileClick)

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

        files = ['txt', 'py', 'java', 'word', 'bin', 'docx', 'doc', 'asm', 'pptx', 'xlxs']
        images = ['jpg', 'bmp', 'png', 'svg']

        if fileName == 'back':
            return 'back'
        elif not '.' in fileName:  # mean that the filename if folder
            return 'folder'
        else:
            typ = fileName.split('.')[1]
            if typ in images:
                return 'img'
            elif typ in files:
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

        #reset the screen
        self.DestroyChildren()

        self.path += '\\' + folder_name
        self.createFilesSizer(self.files[self.path])

    def download_ans(self, ans):
        '''

        :param ans:answer from the server about the download
        :return: show the answer for the user
        '''
        self.frame.status_bar.SetBackgroundColour(wx.BLACK)
        self.frame.status_bar.SetStatusText('')
        if ans == 'ok':
            wx.MessageBox('Downloaded successfully', 'Trive', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Download error, try again later...', 'Trive error', wx.OK | wx.ICON_ERROR)

    def handle_back(self, event):
        '''

        :param event:
        :return: go one folder back from the current path
        '''

        self.DestroyChildren()
        self.path = self.path[:self.path.rindex('\\')]
        self.createFilesSizer(self.files[self.path])

    def add_file(self, file_name):
        '''

        :param file_name:
        :return:
        '''
        self.files[self.path].append(file_name)
        if self.getType(file_name) == 'folder':
            self.files[self.path + '\\' + file_name] = ['back']

        self.DestroyChildren()
        self.createFilesSizer(self.files[self.path])
        # file_sizer = self.createFileSizer(file_name)
        # self.filesSizer.AddSpacer(45)
        # self.filesSizer.Add(file_sizer, 0, flag=wx.ALIGN_CENTER | wx.ALL)

    def get_files(self, answer):
        '''

        :param answer:all the files in the structure
        :return:builds on the screen the file structure
        '''
        self.DestroyChildren()

        current_dir = answer.split(',')[0]
        self.files[current_dir] = []
        lst = answer.split(',')
        lst.remove(current_dir)
        in_top = True
        if self.path == '':
            self.path = current_dir

        for f in lst:
            # means that we enter new directory
            if '\\' in f:
                if in_top:
                    in_top = False
                current_dir =  f
                self.files[current_dir] = []
                if not in_top:
                    self.files[current_dir].append('back')
            # means that f is file or folder in the current directory
            else:
                self.files[current_dir].append(f)

        self.createFilesSizer(self.files[self.path])

        self.got_files = True

    def rename_ans(self, answer):

        ans = answer.split(',')[0]
        file_name = answer.split(',')[1]
        new_name = answer.split(',')[2]

        if ans == 'ok':
            wx.MessageBox('Renamed successfully', 'Trive', wx.OK | wx.ICON_INFORMATION)
            self.rename_file(file_name, new_name)
        else:
            wx.MessageBox('Rename error, try change name or try again later...', 'Trive error', wx.OK | wx.ICON_ERROR)

    def rename_file(self, last_name, new_name):
        '''

        :param file_name:name of file to rename
        :return: change the name on the screen
        '''
        if self.getType(last_name) == 'folder':
            self.change_folder_name(last_name, new_name)
        files: list = self.files[self.path]
        files[files.index(last_name)] = new_name
        self.DestroyChildren()
        self.createFilesSizer(self.files[self.path])

    def delete_file(self, file_name):
        '''

        :param file_name:name of file to delete
        :return: delete the file from the graphic
        '''
        files: list = self.files[self.path]
        files.remove(file_name)
        self.DestroyChildren()
        self.createFilesSizer(self.files[self.path])

    def delete_ans(self, answer):
        '''

        :param answer:answer from the server for the delete
        :return:
        '''
        ans = answer.split(',')[0]
        file_name = answer.split(',')[1]
        if ans == 'ok':
            self.delete_file(file_name)
        else:
            wx.MessageBox('Delete error, try other name or try again later...', 'Trive error', wx.OK | wx.ICON_ERROR)

    def change_folder_name(self, last_name, new_name):
        '''

        :param last_name:
        :param new_name:
        :return:
        '''
        new_dict = {}
        for key in self.files.keys():
            if last_name in key:
                new_key = key.replace(last_name, new_name)
                new_dict[new_key] = self.files[key]
            else:
                new_dict[key] = self.files[key]

        self.files = new_dict
        if last_name in self.path:
            self.path.replace(last_name, new_name)

    def share_ans(self, answer):
        '''

        :param answer:answer from the server
        :return: show the user the answer
        '''
        if answer == 'ok':
            wx.MessageBox('Shared successfully', 'Trive error', wx.OK | wx.ICON_INFORMATION)
        elif answer == 'un':
            wx.MessageBox('Username not exists!', 'Trive error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox('There was an error sharing the file, try again later...!', 'Trive error', wx.OK | wx.ICON_ERROR)\


class AccountPanel(wx.Panel):

    def __init__(self, parent, frame):
        panelDepth = wx.DisplaySize()[0] - 300
        panelLength = wx.DisplaySize()[1] - 350

        screenDepth = wx.DisplaySize()[0]

        # create a new panel
        wx.Panel.__init__(self, parent,pos =((screenDepth - panelDepth)//2, 200), size=(panelDepth, panelLength ), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        #in case that the user change his email
        self.new_email = ''
        self.change_type = ''       #if last change was email -> 'email', otherwise - 'password'
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
        self.try_username = 'Username: ' + self.frame.username

        self.addOptins()
        #create the email text
        self.email = wx.StaticText(self, -1, label=try_email)
        self.email.SetForegroundColour(wx.WHITE)
        self.email.SetFont(self.font)

        # create the username text
        self.username = wx.StaticText(self, -1, label = self.try_username)
        self.username.SetForegroundColour(wx.WHITE)
        self.username.SetFont(self.font)

        self.sizer.Add(user_img,0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(self.email,0,wx.ALL, 5)
        self.sizer.Add(self.username, 0, wx.ALL, 5)
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
        dlg = wx.TextEntryDialog(None, 'Enter new Password: ', 'Change Password', '',style=wx.TE_PASSWORD | wx.OK | wx.CANCEL)

        if dlg.ShowModal() == wx.ID_OK:
            new_password = dlg.GetValue()
            self.frame.q.put(('change_detail', [f'password:{new_password}']))
            pub.subscribe(self.handle_change_details_ans, 'change_details')
            self.change_type = 'password'

    def handle_change_email(self, event):
        '''

        :param event:change email pressed
        :return: get the new email and notify the logic
        '''

        dlg = wx.TextEntryDialog(None, 'Enter new Email: ', 'Change Email', '', style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            new_email = dlg.GetValue()
            self.frame.q.put(('change_detail', [f'email:{new_email}']))
            pub.subscribe(self.handle_change_details_ans, 'change_details')
            self.change_type = 'email'
            self.new_email = new_email

    def handle_logOut(self, event):
        '''

        :param event:
        :return: logout
        '''
        self.parent.frame.q.put(('logout', ''))

    def handle_change_details_ans(self, answer):

        if answer == 'ok':
            wx.MessageBox('change detail successfully', 'Trive', wx.OK | wx.ICON_INFORMATION)
            if self.change_type == 'email':
                self.email.SetLabel(f'Email: {self.new_email}')
        else:
            wx.MessageBox('there was an error changing the detail, try again later', 'Trive error', wx.OK | wx.ICON_ERROR)


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
            self.commandById = {1: 'Download', 2: 'Rename', 3: 'Share', 4: 'Copy', 5: 'Edit' ,6: 'Delete'}
            self.funcById = {1: self.download, 2: self.rename, 3: self.share, 4:self.copy_file, 5:self.edit, 6: self.delete}  #button id -> function that handle if the button selected
        elif self.file_typ == 'image':
            self.commandById = {1: 'Download', 2: 'Rename', 3: 'Share', 4: 'Copy', 6: 'Delete'}
            self.funcById = {1: self.download, 2: self.rename, 3: self.share, 4: self.copy_file, 6: self.delete}
        else :
            self.commandById = { 2: 'Rename', 3: 'Share', 4: 'Copy', 6: 'Delete'}
            self.funcById = { 2: self.rename, 3: self.share, 4: self.copy_file, 6: self.delete}

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
        self.parent.frame.status_bar.SetBackgroundColour(wx.WHITE)
        self.parent.frame.status_bar.SetStatusText(f'Downloading {self.file_name}')

    def rename(self):

        dlg = wx.TextEntryDialog(None, f'Enter new name for the {self.file_typ}(add extention): ', f'Rename {self.file_typ}', '',style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            #check input for the new name
            if self.file_typ == 'folder':
                pattern = "^[A-Za-z1-9_!#&]*$"
                result = re.match(pattern, name)
            elif self.file_typ == 'file':
                pattern = "^[\w,\s-]+\.[A-Za-z1-9_]{1,4}$"
                result = re.match(pattern, name) and self.parent.getType(name) == 'file'
            else:
                pattern = "^[\w,\s-]+\.[A-Za-z1-9_]{1,4}$"
                result = re.match(pattern, name) and self.parent.getType(name) == 'image'

            if result:
                self.parent.frame.q.put(('rename', [self.path + '\\' + self.file_name, name]))
            else:
                wx.MessageBox('Invalid name', 'Trive Error', wx.OK | wx.ICON_ERROR)

    def share(self):

        dlg = wx.TextEntryDialog(None, f'Enter username to share with: ', f'Share {self.file_typ}', '',style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            username = dlg.GetValue()
            self.parent.frame.q.put(('share', [self.path + '\\' + self.file_name, username]))

    def delete(self):
        question = wx.MessageBox('Are you sure you want to delete this file? ', 'Trive Error', wx.YES | wx.NO | wx.ICON_WARNING)
        if question == wx.YES:
            self.parent.frame.q.put(('delete', [self.path + '\\' + self.file_name]))

    def edit(self):
        '''

        :return:handle edit file
        '''
        file_typ = self.file_name.split('.')[1]
        ok_files = ['txt', 'docx', 'xlsx', 'py', 'java', 'asm', 'pptx']
        if file_typ in ok_files:
            self.parent.frame.q.put(('edit', [self.path + '\\' + self.file_name]))
        else:
            wx.MessageBox('Trive cant edit this file!', 'Trive Error', wx.OK | wx.ICON_ERROR)

    def copy_file(self):
        '''

        :return:change the now coping file in the parent
        '''
        self.parent.copying = self.path + '\\' + self.file_name


if __name__ == '__main__':
    q = queue.Queue()
    app = wx.App()
    frame = MyFrame(q)
    app.MainLoop()