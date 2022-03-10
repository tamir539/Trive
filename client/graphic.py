import wx
import wx.lib.scrolledpanel as scrolled
from pubsub import pub
import queue
import re

class MyFrame(wx.Frame):
    def __init__(self, q):
        '''

        :param q:queue to talk with the logic
        username -> username of the connected user
        email -> email of the connected user
        status_bar -> status bar of the frame
        main_panel -> main panel
        '''
        # create the frame
        super(MyFrame, self).__init__(None, title="Trive", size=wx.DisplaySize())

        self.username = ''
        self.email = ''
        self.status_bar = self.CreateStatusBar(1)
        self.status_bar.SetBackgroundColour(wx.BLACK)

        #  create main panel - to put on the others panels
        self.main_panel = MainPanel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.main_panel, 1, wx.EXPAND)
        self.q = q

        #  loc = wx.IconLocation('draws\\logo.jpg', wx.BITMAP_TYPE_ICO)
        #  self.SetIcon(loc)

        #  arrange the frame
        self.SetSizer(box)
        self.Layout()
        self.Show()
        self.Maximize()

        pub.subscribe(self.disconnect, 'disconnect')

    def disconnect(self):
        '''

        :return:notify the user that the server isnt availabale
        '''
        wx.MessageBox('Server under maintnence, login later', 'Trive error', wx.OK | wx.ICON_ERROR)
        self.Destroy()

    def finish_edit(self):
        '''

        :return: notify that the edit finish
        '''
        self.main_panel.loby.editing = False


class MainPanel(wx.Panel):
    '''
    class that create the main layout
    '''
    def __init__(self, parent):
        '''

        login -> the login panel
        registration -> registration panel
        loby -> loby panel
        '''

        wx.Panel.__init__(self, parent)

        self.frame = parent
        self.SetBackgroundColour(wx.BLACK)
        self.v_box = wx.BoxSizer()

        #  create object for each panel
        self.login = LoginPanel(self, self.frame)
        self.registration = RegisterPanel(self, self.frame)
        self.loby = LobyPanel(self,self.frame)

        self.v_box.Add(self.login)

        #  The first panel to show
        self.login.Show()
        self.SetSizer(self.v_box)
        self.Layout()


class LoginPanel(wx.Panel):

    '''
        class that create the login layout
    '''
    def __init__(self, parent, frame):
        '''

        username -> username of the connected user
        '''
        #  create a new panel
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, size=wx.DisplaySize(), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        self.username = ''
        self.__create_screen__()

    def __create_screen__(self):

        #  create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        #  change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        # add the Trive logo
        png = wx.Image('draws\\logo.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        trive = wx.StaticBitmap(self, -1, png, (650, -2), (png.GetWidth(), png.GetHeight()))

        #  wait for answer from the logic
        pub.subscribe(self.handle_answer, 'login')

        # font
        self.font = wx.Font(22, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        # create sizer for the username logo and textfield
        name_box = wx.BoxSizer(wx.HORIZONTAL)

        self.create_username_field()

        #  add the user logo
        user = wx.Image('draws\\user.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        user_logo = wx.StaticBitmap(self, -1, user, (565, 275), (user.GetWidth(), user.GetHeight()))

        # update the username sizer
        name_box.Add(user_logo, 0, wx.ALL, 0)
        name_box.Add(self.username_field, 0, wx.ALL, 5)

        # create sizer for the password
        pass_box = wx.BoxSizer(wx.HORIZONTAL)

        self.create_password_field()

        #  add the fingerprint logo
        finger = wx.Image('draws\\finger.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        finger_logo = wx.StaticBitmap(self, -1, finger, (565, 383), (finger.GetWidth(), finger.GetHeight()))

        # update the password sizer
        pass_box.Add(finger_logo, 0, wx.ALL, 0)
        pass_box.Add(self.passWordField, 0, wx.ALL, 5)

        #  add all elements to sizer
        self.sizer.Add(trive,0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(100)
        self.sizer.Add(name_box,0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(pass_box,0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(20)
        self.add_buttons()

        #  arrange the screen
        self.SetSizer(self.sizer)
        self.Layout()
        self.Hide()

    def error_msg(self, msg):
        '''

        :param msg:massage to shoe in the error
        :return: create and shoe the error massage
        '''
        wx.MessageBox(msg, 'Trive Error', wx.OK | wx.ICON_HAND )

    def add_buttons(self):
        '''

        :return: add all the buttons
        '''

        self.create_btn('Login', self.handle_login, (400, 40))

        self.create_btn('Not a member? sign up!', self.handle_reg, (400, 40))

        #  size down the font for the forgot your password button
        self.font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        self.create_btn('forgot your password?', self.handle_forgot_password, (250, 30))

    def create_btn(self, msg, func, size):
        '''

        :param msg: the msg to put in the button
        :param func: function to bind to the button
        :param size: the size of the button
        :return:
        '''
        #  create the button
        btn = wx.Button(self, wx.ID_ANY, label=msg, size=size)
        #  design the button
        if msg == 'Login':
            btn.Font = self.font.Bold()
        elif msg == 'forgot your password?':
            btn.Font = self.font.MakeUnderlined()
        else:
            btn.Font = self.font
        btn.BackgroundColour = wx.BLACK
        btn.ForegroundColour = wx.GREEN
        btn.Bind(wx.EVT_BUTTON, func)
        self.sizer.Add(btn, 0, wx.CENTER | wx.ALL, 5)

    def create_username_field(self):
        '''

        :return:create and design the userName textField
        '''
        # create the tet field
        self.username_field = wx.TextCtrl(self, 10, name="username", style=wx.TEXT_ATTR_BULLET_STYLE_ROMAN_UPPER, size=(500, 38))

        #  design the username text field
        self.username_field.SetHint('username:')
        self.username_field.SetBackgroundColour(wx.BLACK)
        self.username_field.SetForegroundColour(wx.WHITE)
        self.username_field.Font = self.font

    def create_password_field(self):
        '''

        :return:create and design the password textField
        '''
        #  create the password text field
        self.passWordField = wx.TextCtrl(self, -1, name="password", style=wx.TE_PASSWORD, size=(500, 38))

        #  design the password text field
        self.passWordField.SetHint('password:')
        self.passWordField.SetBackgroundColour(wx.BLACK)
        self.passWordField.SetForegroundColour(wx.WHITE)
        self.passWordField.SetFont(self.font)

    def handle_login(self, event):
        '''

        :param event:event that happend on the screen
        :return:take care the event when pressing login button
        '''
        username = self.username_field.GetValue()
        password = self.passWordField.GetValue()

        if not username or not password:
            self.error_msg('You must enter username and password!')
        else:
            self.username = username
            self.frame.q.put(('login', [username, password]))

    def handle_reg(self, event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        self.Hide()
        self.parent.registration.Show()

    def handle_forgot_password(self, event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing forgot password
        '''
        dlg = wx.TextEntryDialog(None, 'Enter username: ','get new password to your email', '',
                                 style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            email = dlg.GetValue()
            self.frame.q.put(('forgot_password', [email]))
            wx.MessageBox('If the username exists, he will get email with your new password...')

    def handle_answer(self, answer):
        '''

        :param answer: answer from the server
        :return: if answer is "ok" go to the lobby, otherwise error msg
        '''
        ans = answer.split(',')[0]
        if ans == 'no':
            self.error_msg('Wrong username or password')
        elif ans == 'ac':
            self.error_msg('You already connected from other device!')
        elif ans == 'ok':
            email = answer.split(',')[1]
            self.frame.username = self.username
            self.frame.email = email
            # move to loby
            self.Hide()
            self.parent.loby.Show()
        else:
            self.error_msg('This ip has been blocked!')
            self.frame.Destroy()


class RegisterPanel(wx.Panel):
    '''
        class that create the register panel
    '''

    def __init__(self, parent, frame):
        #  create a new panel
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, size=wx.DisplaySize(), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        self.__create_screen__()

    def __create_screen__(self):
        #  create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        #  change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        #  add the Trive logo
        png = wx.Image('draws\\logo.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        logo = wx.StaticBitmap(self, -1, png, (650, -2), (png.GetWidth(), png.GetHeight()))

        #  talk with the logic client
        pub.subscribe(self.handle_answer, 'register')

        #  font for the text
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        #  create sizer for the email
        email_box = wx.BoxSizer(wx.HORIZONTAL)

        self.create_email_field()

        #  add the email logo
        email = wx.Image('draws\\email.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        email_logo = wx.StaticBitmap(self, -1, email, (565, 275), (email.GetWidth(), email.GetHeight()))

        # update the email sizer
        email_box.Add(email_logo, 0, wx.ALL, 0)
        email_box.Add(self.email_field, 0, wx.ALL, 0)

        #  create sizer for the username
        name_box = wx.BoxSizer(wx.HORIZONTAL)

        self.create_username_field()

        #  add the user logo
        user = wx.Image('draws\\user.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        user_logo = wx.StaticBitmap(self, -1, user, (565, 275), (user.GetWidth(), user.GetHeight()))

        #  update the username sizer
        name_box.Add(user_logo, 0, wx.ALL, 0)
        name_box.Add(self.username_field, 0, wx.ALL, 5)

        #  create sizer for the password
        pass_box = wx.BoxSizer(wx.HORIZONTAL)

        self.create_password_field()

        #  add the fingerprint logo
        finger = wx.Image('draws\\finger.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        finger_logo = wx.StaticBitmap(self, -1, finger, (565, 383), (finger.GetWidth(), finger.GetHeight()))

        # update the password sizer
        pass_box.Add(finger_logo, 0, wx.ALL, 0)
        pass_box.Add(self.password_field, 0, wx.ALL, 5)

        # add all the elements to the main sizer
        self.sizer.Add(logo, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(100)
        self.sizer.Add(email_box, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(name_box, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(pass_box, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.AddSpacer(20)
        self.add_buttons()

        #  arrange the screen
        self.SetSizer(self.sizer)
        self.Layout()
        self.Hide()

    def error_msg(self, msg):
        '''

        :param msg:massage to shoe in the error
        :return: create and shoe the error massage
        '''
        wx.MessageBox(msg, 'Trive Error', wx.OK | wx.ICON_HAND )

    def add_buttons(self):
        '''

        :return: add all the buttons
        '''

        self.create_btn('Register', self.handle_reg, (400, 40))

        self.create_btn('Login', self.handle_login, (400, 40))

    def create_btn(self, msg, func, size):
        '''

        :param msg: the msg to put in the button
        :param func: function to bind to the button
        :param size: size of the new button
        :return:creates the new button
        '''
        #  create the button
        btn = wx.Button(self, wx.ID_ANY, label=msg, size=size)
        #  design the button
        if msg == 'Register':
            btn.Font = self.font.Bold()
        else:
            btn.Font = self.font
        btn.BackgroundColour = wx.BLACK
        btn.ForegroundColour = wx.GREEN
        btn.Bind(wx.EVT_BUTTON, func)
        self.sizer.Add(btn, 0, wx.CENTER | wx.ALL, 5)

    def create_username_field(self):
        '''

        :return:create and design the userName textField
        '''
        # create the tet field
        self.username_field = wx.TextCtrl(self, 10, name="username", style=wx.TEXT_ATTR_BULLET_STYLE_ROMAN_UPPER, size=(500, 38))

        #  design the username text field
        self.username_field.SetHint('username:')
        self.username_field.SetBackgroundColour(wx.BLACK)
        self.username_field.SetForegroundColour(wx.WHITE)
        self.username_field.Font = self.font

    def create_password_field(self):
        '''

        :return:create and design the password textField
        '''
        #  create the password text field
        self.password_field = wx.TextCtrl(self, -1, name="password", style=wx.TE_PASSWORD, size=(500, 38))

        #  design the password text field
        self.password_field.SetHint('password:')
        self.password_field.SetBackgroundColour(wx.BLACK)
        self.password_field.SetForegroundColour(wx.WHITE)
        self.password_field.SetFont(self.font)

    def create_email_field(self):
        '''

        :return:create and design the email textField
        '''
        #  create the email text field
        self.email_field = wx.TextCtrl(self, -1, name="email", size=(500, 38))

        #  design the email text field
        self.email_field.SetFont(self.font)
        self.email_field.SetHint('email:')
        self.email_field.SetBackgroundColour(wx.BLACK)
        self.email_field.SetForegroundColour(wx.WHITE)

    def handle_reg(self, event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        #  mean someone create account
        username = self.username_field.GetValue()
        password = self.password_field.GetValue()
        email = self.email_field.GetValue()

        # check email input
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        result = re.match(pattern, email)

        if not username or not password or not email:
            self.error_msg('You must enter username, password and email')
        elif not result:
            wx.MessageBox('Invalid Email', 'Trive Error', wx.OK | wx.ICON_ERROR)
        else:
            self.username = username
            self.parent.login.username = username
            self.frame.username = self.username
            self.frame.email = email
            self.Hide()
            self.parent.login.Hide()
            self.frame.q.put(('register', [email, username, password]))
            self.frame.q.put(('login', [username, password]))

    def handle_login(self, event):
        '''

        :param event: event that happend on the screen
        :return:take care the event when pressing registration button and calling the registration screen
        '''
        self.Hide()
        self.parent.login.Show()

    def handle_answer(self, answer):
        '''

        :param answer: answer from the server
        :return: show the answer to the user
        '''
        if answer == 'un':
            self.error_msg('This username is already taken')
        else:
            wx.MessageBox(f'Welcome {self.username}!', 'Trive', wx.OK | wx.ICON_NONE)
            self.Hide()


class LobyPanel(wx.Panel):
    '''
    class to the loby screen(contains files panel and account panel)
    '''
    def __init__(self, parent, frame):
        '''

        in_account -> true - we are in account panel, false otherwise
        account -> the account panel
        scroll_files -> the files panel
        uploading -> 'True' - we are in upload, 'false' otherwise
        editing  -> 'True' - we are in edit, 'false' otherwise
        new_folder_name -> when create new folder -> her new name
        path_to_show -> the current path of the user

        '''
        #  create a new panel
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, size=wx.DisplaySize(), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        self.in_account = False
        self.account = None
        self.scroll_files = None
        self.uploading = False
        self.editing = False
        self.new_folder_name = ''
        self.path_to_show = None
        self.Hide()
        self.__create_screen__()

    def __create_screen__(self):
        #  create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        #  change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        #  add the Trive logo
        png = wx.Image('draws\\logo.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        logo = wx.StaticBitmap(self, -1, png, (650, -2), (png.GetWidth(), png.GetHeight()))

        #  font for the text
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        # wait for answer from the logic to upload
        pub.subscribe(self.uplod_answer, 'upload')

        # create the files scroller
        self.scroll_files = ScrollFilesPanel(self, self.parent.frame)

        #  create the files scroller
        self.account = AccountPanel(self, self.parent.frame)

        self.path_to_show = wx.StaticText(self, -1, ' in: Trive', (100, 30))
        self.path_to_show.SetForegroundColour(wx.GREEN)
        self.path_to_show.SetFont(self.font)

        created_by = wx.StaticText(self, -1, '©Tamir Burstein', (100, 20))
        created_by.SetForegroundColour(wx.WHITE)

        # add the options
        self.add_options()

        # add all the elements to the sizer
        self.sizer.Add(created_by, 0, wx.LEFT | wx.ALL, 5)
        self.sizer.Add(logo, 0, wx.CENTER | wx.ALL, 5)
        self.sizer.Add(self.path_to_show, 0, wx.LEFT | wx.ALL, 5)
        self.sizer.AddSpacer(wx.DisplaySize()[1] - png.GetHeight() - 210)
        self.sizer.Add(self.options_sizer, 0, wx.CENTER | wx.ALL)


        #  arrange the screen
        self.SetSizer(self.sizer)
        self.Layout()

    def add_options(self):
        '''

        :return: add all the optins in the buttom to sizer
        '''
        self.options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.options_sizer.AddSpacer(80)

        #  create the paste button
        self.create_btn(self.options_sizer, "Paste here", self.handle_paste)

        #  create the account button
        self.account_or_files = self.create_btn(self.options_sizer, "Account", self.handle_account)

        #  create the upload button
        self.create_btn(self.options_sizer, "Upload file", self.handle_upload)

        #  create the add folder button
        self.create_btn(self.options_sizer, "Create folder", self.handle_create_folder)

    def create_btn(self, sizer, msg, func):
        '''

        :param sizer: sizer to put the Btn in
        :param msg: the msg to put in the button
        :param func: function to bind to the button
        :return:
        '''
        #  create the button
        btn = wx.Button(self, wx.ID_ANY, label=msg, size=(250, 40))
        #  design the button
        btn.Font = self.font
        btn.BackgroundColour = wx.BLACK
        btn.ForegroundColour = wx.GREEN
        btn.Bind(wx.EVT_BUTTON, func)
        sizer.Add(btn)
        sizer.AddSpacer(50)
        return btn

    def handle_upload(self, event):
        '''

        :param event:  means  the upload btn pressed
        :return:
        '''
        if 'recycle' in self.scroll_files.path or 'shared' in self.scroll_files.path:
            self.error_msg('Cant upload here')
        else:
            open_file_dialog = wx.FileDialog(self, "Open", "", "", "",wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            open_file_dialog.ShowModal()
            # path of the selected file
            path = open_file_dialog.GetPath()
            if path != '':
                # name of the selected file
                file_name = path[path.rindex('\\') + 1:]
                open_file_dialog.Destroy()
                if self.uploading:
                    self.error_msg('Wait the other upload to finish!')
                # check that the file isnt allready exists
                elif file_name in self.scroll_files.files[self.scroll_files.path]:
                    self.error_msg('File allready exists')
                else:
                    # update the status_bar that upload started
                    self.frame.status_bar.SetBackgroundColour(wx.WHITE)
                    self.frame.status_bar.SetStatusText(f'Uploading {file_name}')
                    self.frame.q.put(('upload', [path, self.scroll_files.path]))
                    self.uploading = True

    def get_type(self, file_name):
        '''

        :param file_name: name of file
        :return:  "img" if the file is some image, "file" if the file is some text file, "folder" if the fileName if folder, "no"
        '''

        files = ['txt', 'py', 'java', 'word', 'bin', 'docx', 'doc', 'asm', 'pptx', 'xlsx']
        images = ['jpg', 'bmp', 'png', 'svg']

        if '.' in file_name:
            typ = file_name.split('.')[1]
            if typ in images:
                return 'img'
            elif typ in files:
                return 'file'
            else:
                return 'unknown'
        #  mean that the filename if folder
        else:
            return 'folder'

    def handle_create_folder(self, event):
        '''

        :param event:  means  the upload file btn pressed
        :return:
        '''

        if 'recycle' in self.scroll_files.path or 'shared' in self.scroll_files.path:
            wx.MessageBox('Cant create folder here', 'Trive error', wx.OK | wx.ICON_ERROR)
        else:
            dlg = wx.TextEntryDialog(None, 'Enter name for the folder: ', 'Create folder', '',style=wx.TextEntryDialogStyle)

            if dlg.ShowModal() == wx.ID_OK:
                self.new_folder_name = dlg.GetValue()
                if self.new_folder_name == 'shared':
                    wx.MessageBox('Unavailabale name', 'Trive Error', wx.OK | wx.ICON_ERROR)
                else:
                    #  calculate the virtual path
                    path = self.scroll_files.path + '\\' + self.new_folder_name
                    self.frame.q.put(('create_folder', [path]))
                    pub.subscribe(self.handle_create_folder_answer, 'create_folder')

    def handle_account(self, event):
        '''

        :param event:  means the account btn pressed
        :return:
        '''
        if self.in_account:
            self.account.Hide()
            self.scroll_files.Show()
            self.account_or_files.SetLabel('Account')
        else:
            self.account.Show()
            self.scroll_files.Hide()
            # set the username and email of the user
            self.account.username.SetLabel(f'Username: {self.frame.username}')
            self.account.email.SetLabel(f'Email: {self.frame.email}')
            self.account_or_files.SetLabel('Files')
        self.in_account = not self.in_account

    def handle_create_folder_answer(self, answer):
        '''

        :param answer:answer from the server
        :return:
        '''
        if answer == 'ok':
            wx.MessageBox(f'Folder {self.new_folder_name} created successfuly!', 'Trive', wx.OK | wx.ICON_INFORMATION)
            self.scroll_files.add_file(self.new_folder_name)
            self.new_folder_name = ''
        else:
            wx.MessageBox(f'There was an error in creating {self.new_folder_name} folder', 'Trive Error', wx.OK | wx.ICON_ERROR)

    def error_msg(self, msg):
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
            self.scroll_files.add_file(file_name)
        else:
            wx.MessageBox(f'There was an error in uploading {file_name}', 'Trive Error',wx.OK | wx.ICON_ERROR)
        self.uploading = False

    def handle_paste(self, event):
        '''

        :param event:
        :return: paste the last copyed file in this path
        '''
        copyied = self.scroll_files.copying
        if copyied == '':
            self.error_msg('No file or folder has been selected')
        elif 'recycle' in self.scroll_files.path or 'shared' in self.scroll_files.path:
            self.error_msg('Cant paste here')
        else:
            self.frame.q.put(('add_to_folder', [copyied, self.scroll_files.path]))
            pub.subscribe(self.add_to_folder_answer, 'add_to_folder')

    def add_to_folder_answer(self, answer):
        '''

        :param answer:answer from the server
        :return:show the answer to the client
        '''
        if answer == 'ok':
            # path to the file that last copyied
            copyied = self.scroll_files.copying
            copyied_name = copyied[copyied.rindex('\\') + 1:]
            # add the file to the selected folder
            self.scroll_files.add_file(copyied_name)
        else:
            self.error_msg('There was an error with pasting the file here')


class ScrollFilesPanel(scrolled.ScrolledPanel):
    '''
        class that show all the top level files on the screen
    '''
    def __init__(self, parent, frame):
        '''

        files -> dictionay of folder path : all the files in this path
        got_files -> "true" -> all the files names recived, "false" otherwise
        path -> the virtual path we are in
        copying -> the vurtual path of the last file that copiyed

        '''
        panel_depth = wx.DisplaySize()[0] - 300
        panel_length = wx.DisplaySize()[1] - 400
        screen_depth = wx.DisplaySize()[0]

        #  create a new panel
        scrolled.ScrolledPanel.__init__(self, parent,pos =((screen_depth - panel_depth)/2, 250), size=(panel_depth, panel_length ), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        self.files = {}
        self.got_files = False
        self.path = ''
        self.copying = ''
        self.Hide()
        self.__create_screen__()

    def __create_screen__(self):
        #  change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        #  font for the text
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        # wait for answers from the logic
        pub.subscribe(self.download_ans, 'finish_download')
        pub.subscribe(self.get_files, 'get_all_files')
        pub.subscribe(self.rename_ans, 'rename')
        pub.subscribe(self.delete_ans, 'delete')
        pub.subscribe(self.share_ans, 'share')

        self.Show()

    def create_files_sizer(self, files):
        '''

        :param index: index in self.files dictionary
        :return: show in the screen the files that are on top of the directories
        '''
        # vetrical sizer for all the horizontal sizers
        place_files_sizer = wx.BoxSizer(wx.VERTICAL)
        files_sizer = wx.BoxSizer(wx.HORIZONTAL)

        items_in_sizer_count = 0
        char_count = 0
        place_files_sizer.AddSpacer(20)

        for file in files:
            #  check that there are not more then 7 files in a row
            if char_count + len(file) > 70 or items_in_sizer_count > 6:
                # mean the horizontal sizer full -> create new one and add this one to the vertical of the horizontals
                place_files_sizer.Add(files_sizer)
                files_sizer = wx.BoxSizer(wx.HORIZONTAL)
                place_files_sizer.AddSpacer(50)
                items_in_sizer_count = 0
                char_count = 0

            files_sizer.AddSpacer(45)
            files_sizer.Add(self.create_file_sizer(file), 0, flag=wx.ALIGN_CENTER | wx.ALL)
            items_in_sizer_count += 1
            char_count += len(file)

        place_files_sizer.Add(files_sizer)
        self.SetSizer(place_files_sizer)
        self.SetupScrolling()

    def create_file_sizer(self, file):
        '''
        @:param file: name of the file
        :return: create sizer for file(file image, file name)
        '''
        # sizer to the current file
        file_sizer = wx.BoxSizer(wx.VERTICAL)

        #  add the file\image\folder logo
        img = wx.Image(f'draws\\{self.get_type(file)}.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        file_img = wx.StaticBitmap(self, -1, img, (650, -2), (img.GetWidth(), img.GetHeight()))
        file_img.SetName(file)

        file_sizer.Add(file_img, 0, wx.CENTER | wx.ALL)

        if self.get_type(file) == 'folder':
            file_img.Bind(wx.EVT_LEFT_DCLICK, self.get_into_folder)

        if self.get_type(file) == 'back':
            file_img.Bind(wx.EVT_LEFT_DOWN, self.handle_back)

        elif file != 'shared' and file != 'recycle':
            file_img.Bind(wx.EVT_RIGHT_DOWN, self.on_file_click)

        # add the name of the file\image\folder
        file_name = wx.StaticText(self, -1, label=file)
        file_name.SetForegroundColour(wx.WHITE)
        file_name.SetFont(self.font)

        file_sizer.Add(file_name, 0, wx.CENTER | wx.ALL)
        return file_sizer

    def get_type(self, file_name):
        '''

        :param file_name: name of file
        :return:  "image" if the file is some image, "file" if the file is some text file, "folder" if the fileName if folder, "no"
        '''

        files = ['txt', 'py', 'java', 'word', 'bin', 'docx', 'doc', 'asm', 'pptx', 'xlsx']
        images = ['jpg', 'bmp', 'png', 'svg']

        if file_name == 'back':
            return 'back'
        elif '.' in file_name:  # mean that the filename if folder
            typ = file_name.split('.')[1]
            if typ in images:
                return 'image'
            elif typ in files:
                return 'file'
            else:
                return 'unknown'
        else:
            return 'folder'

    def on_file_click(self, event):
        '''

        :param event:event mean that file pressed
        :return:change the current pressed file of the class
        '''
        widget = event.GetEventObject()
        file_name = widget.GetName()
        self.PopupMenu(OptionsMenu(self, self.get_type(file_name),file_name, self.path))

    def get_into_folder(self, event):
        '''

        :param event:
        :return: show the files that in the folder on the screen
        '''

        widget = event.GetEventObject()
        folder_name = widget.GetName()

        # reset the screen
        self.DestroyChildren()

        self.path += '\\' + folder_name
        self.create_files_sizer(self.files[self.path])
        current_show = self.parent.path_to_show.GetLabel()
        self.parent.path_to_show.SetLabel(current_show + '\\' + folder_name)

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
        current_show = self.parent.path_to_show.GetLabel()
        self.parent.path_to_show.SetLabel(current_show[:current_show.rindex('\\')])
        self.create_files_sizer(self.files[self.path])

    def add_file(self, file_name):
        '''

        :param file_name:
        :return:
        '''
        self.files[self.path].append(file_name)
        if self.get_type(file_name) == 'folder':
            self.files[self.path + '\\' + file_name] = ['back']

        self.DestroyChildren()
        self.create_files_sizer(self.files[self.path])

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
            #  means that we enter new directory
            if '\\' in f:
                if in_top:
                    in_top = False
                current_dir = f
                self.files[current_dir] = []
                if not in_top:
                    self.files[current_dir].append('back')
            #  means that f is file or folder in the current directory
            else:
                self.files[current_dir].append(f)

        self.create_files_sizer(self.files[self.path])

        self.got_files = True

    def rename_ans(self, answer):
        '''

        :param answer: answer to the rename file
        :return: notify the user the answer
        '''
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

        :param file_name: name of file to rename
        :return: change the name on the screen
        '''
        if self.get_type(last_name) == 'folder':
            self.change_folder_name(last_name, new_name)
        files: list = self.files[self.path]
        files[files.index(last_name)] = new_name
        # reset the screen
        self.DestroyChildren()
        #  create the screen
        self.create_files_sizer(self.files[self.path])

    def delete_file(self, file_name):
        '''

        :param file_name:name of file to delete
        :return: delete the file from the graphic
        '''
        files: list = self.files[self.path]
        files.remove(file_name)
        #  reset the screen
        self.DestroyChildren()
        # create the screen
        self.create_files_sizer(self.files[self.path])

    def delete_ans(self, answer):
        '''

        :param answer:answer from the server for the delete
        :return:
        '''
        ans = answer.split(',')[0]
        # name of the file that deleted
        file_name = answer.split(',')[1]
        if ans == 'ok':
            self.delete_file(file_name)
            wx.MessageBox(f'{file_name} deleted successfully!', 'Trive error', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Delete error, try other name or try again later...', 'Trive error', wx.OK | wx.ICON_ERROR)

    def change_folder_name(self, last_name, new_name):
        '''

        :param last_name:
        :param new_name:
        :return:rename the folder securly
        '''
        new_dict = {}
        # every path that contains the lsat name: rename it to the new name
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
        else:
            wx.MessageBox('There was an error sharing the file, try again later...!', 'Trive error', wx.OK | wx.ICON_ERROR)\



class AccountPanel(wx.Panel):
    '''
    panel to the account
    '''
    def __init__(self, parent, frame):
        '''

        new_email -> new email if the user changed his email
        change_type ->  if last change was email -> 'email', otherwise - 'password'
        '''
        panel_depth = wx.DisplaySize()[0] - 300
        panel_length = wx.DisplaySize()[1] - 350

        screen_depth = wx.DisplaySize()[0]

        #  create a new panel
        wx.Panel.__init__(self, parent,pos =((screen_depth - panel_depth)//2, 200), size=(panel_depth, panel_length), style=wx.SIMPLE_BORDER)
        self.frame = frame
        self.parent = parent
        self.new_email = ''
        self.change_type = ''
        self.Hide()
        self.__create_screen__()

    def __create_screen__(self):
        #  create the main sizer of the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        #  change background colour to black
        self.SetBackgroundColour(wx.BLACK)

        #  font for the text
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        # add the account logo
        user = wx.Image('draws\\userForLoby.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        user_img = wx.StaticBitmap(self, -1, user,  pos=(wx.DisplaySize()[0] - wx.DisplaySize()[0]//7, 30),
                                   size=(user.GetWidth(), user.GetHeight()))
        # all the options to the sizer
        options_sizer = self.add_options()

        # create the email text
        self.email = wx.StaticText(self, -1, label= '')
        self.email.SetForegroundColour(wx.WHITE)
        self.email.SetFont(self.font)

        #  create the username text
        self.username = wx.StaticText(self, -1, label = '')
        self.username.SetForegroundColour(wx.WHITE)
        self.username.SetFont(self.font)

        # add all the elements to the main sizer
        self.sizer.Add(user_img,0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(self.email,0,wx.ALL, 5)
        self.sizer.Add(self.username, 0, wx.ALL, 5)
        self.sizer.AddSpacer(100)
        self.sizer.Add(options_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        #  arrange the screen
        self.SetSizer(self.sizer)
        self.Layout()

    def add_options(self):
        '''

        :return: add all the optins in the buttom to sizer
        '''
        options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        options_sizer.AddSpacer(80)

        #  create the change password button
        self.create_btn(options_sizer, "Change password", self.handle_change_password)

        #  create the change email button
        self.create_btn(options_sizer, "Change email", self.handle_change_email)
        return options_sizer

    def create_btn(self, sizer, msg, func):
        '''

        :param sizer: sizer to put the Btn in
        :param msg: the msg to put in the button
        :param func: function to bind to the button
        :return:
        '''
        #  create the button
        btn = wx.Button(self, wx.ID_ANY, label=msg, size=(250, 40))
        #  design the button
        btn.Font = self.font
        btn.BackgroundColour = wx.BLACK
        btn.ForegroundColour = wx.GREEN
        btn.Bind(wx.EVT_BUTTON, func)
        sizer.Add(btn)
        sizer.AddSpacer(50)

    def handle_change_password(self, event):
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

    def handle_change_details_ans(self, answer):
        '''

        :param answer:answer to the change details
        :return: show the answer to the user
        '''
        if answer == 'ok':
            wx.MessageBox('change detail successfully', 'Trive', wx.OK | wx.ICON_INFORMATION)
            if self.change_type == 'email':
                self.email.SetLabel(f'Email: {self.new_email}')
        else:
            wx.MessageBox('There was an error changing the detail, try again later', 'Trive error', wx.OK | wx.ICON_ERROR)


class OptionsMenu(wx.Menu):

    def __init__(self, parent, file_typ, file_name, path):
        '''

        file_name -> name of the file that the options for
        file_typ -> type of the file that the options for
        path -> path of the file that the options for
        font -> text font
        command_by_id -> dictionary of the command to do and the value is the id
        func_by_id -> dictionary of the id that selected and the function to call to
        '''
        super(OptionsMenu, self).__init__()

        self.parent = parent
        self.file_name = file_name
        self.file_typ = file_typ
        self.path = path
        self.font = None
        self.command_by_id = None
        self.func_by_id = None
        self.createOptions()

    def createOptions(self):
        '''

        :return: create all the options
        '''
        # font for the text
        self.font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)

        self.Bind(wx.EVT_MENU, self.get_chosen)

        if self.file_typ == 'file':
            self.command_by_id = {1: 'Download', 2: 'Rename', 3: 'Share', 4: 'Copy', 5: 'Edit', 6: 'Delete'}
            self.func_by_id = {1: self.download, 2: self.rename, 3: self.share, 4:self.copy_file, 5: self.edit,
                               6: self.delete}  # button id -> function that handle if the button selected
        elif self.file_typ == 'image' or self.file_typ == 'unknown':
            self.command_by_id = {1: 'Download', 2: 'Rename', 3: 'Share', 4: 'Copy', 6: 'Delete'}
            self.func_by_id = {1: self.download, 2: self.rename, 3: self.share, 4: self.copy_file, 6: self.delete}
        else:
            self.command_by_id = {2: 'Rename', 3: 'Share', 4: 'Copy', 6: 'Delete'}
            self.func_by_id = {2: self.rename, 3: self.share, 4: self.copy_file, 6: self.delete}

        for command_id in self.command_by_id.keys():
            self.create_option(command_id)

    def create_option(self, id):
        '''

        :param id: id for the option
        :return: creates the option and add to the menu
        '''
        popmenu = wx.MenuItem(self, id, self.command_by_id[id])
        popmenu.SetBackgroundColour(wx.BLACK)
        popmenu.SetTextColour(wx.WHITE)
        popmenu.SetFont(self.font)
        self.Append(popmenu)

    def get_chosen(self, event):
        '''

        :param event:
        :return: return the id of the selected command
        '''
        command_id = event.GetId()
        self.func_by_id[command_id]()

    def download(self):
        '''

        :return: notify the logic that the download button pressed
        '''
        self.parent.frame.q.put(('download', [self.path + '\\' + self.file_name]))
        self.parent.frame.status_bar.SetBackgroundColour(wx.WHITE)
        self.parent.frame.status_bar.SetStatusText(f'Downloading {self.file_name}')

    def rename(self):
        '''

        :return: check the input and notify the logic that the rename button pressed
        '''
        # get new name to the file
        dlg = wx.TextEntryDialog(None, f'Enter new name for the {self.file_typ}(add extention): ', f'Rename {self.file_typ}', '',style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            # check input for the new name
            if self.file_typ == 'folder':
                pattern = "^[A-Za-z1-9_!# &]*$"
                result = re.match(pattern, name)
            elif self.file_typ == 'file':
                pattern = "^[\w,\s-]+\.[A-Za-z1-9_]{1,4}$"
                result = re.match(pattern, name) and self.parent.get_type(name) == 'file'
            else:
                pattern = "^[\w,\s-]+\.[A-Za-z1-9_]{1,4}$"
                result = re.match(pattern, name) and self.parent.get_type(name) == 'image'
            if result:
                self.parent.frame.q.put(('rename', [self.path + '\\' + self.file_name, name]))
            else:
                wx.MessageBox('Invalid name', 'Trive Error', wx.OK | wx.ICON_ERROR)

    def share(self):
        '''

        :return:notify the logic that the share file pressed
        '''
        # get the username to share with
        dlg = wx.TextEntryDialog(None, f'Enter username to share with: ', f'Share {self.file_typ}', '',style=wx.TextEntryDialogStyle)

        if dlg.ShowModal() == wx.ID_OK:
            username = dlg.GetValue()
            self.parent.frame.q.put(('share', [self.path + '\\' + self.file_name, username]))

    def delete(self):
        '''

        :return: notify the logic that the delete file pressed
        '''
        question = wx.MessageBox('Are you sure you want to delete this file? ', 'Trive Error', wx.YES | wx.NO | wx.ICON_WARNING)
        if question == wx.YES:
            self.parent.frame.q.put(('delete', [self.path + '\\' + self.file_name]))

    def edit(self):
        '''

        :return:handle edit file
        '''
        file_typ = self.file_name.split('.')[1]
        ok_files = ['txt', 'docx', 'xlsx', 'py', 'pptx']
        if self.parent.parent.editing:
            wx.MessageBox('Cant edit 2 files...', 'Trive error', wx.OK | wx.ICON_ERROR)
        elif file_typ in ok_files:
            self.parent.frame.q.put(('edit', [self.path + '\\' + self.file_name]))
            self.parent.parent.editing = True
        else:
            wx.MessageBox('We cant edit this file yet :(', 'Trive Error', wx.OK | wx.ICON_ERROR)

    def copy_file(self):
        '''

        :return:change the now coping file in the parent
        '''
        self.parent.copying = self.path + '\\' + self.file_name