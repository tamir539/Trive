import sqlite3


class DB:

    def __init__(self, db_name):
        '''

        db_name: name to the data_base
        users_table: name of the users table
        ips_table: name of the ips_table
        conn: the connection to the data_base
        cursor: handler to the data_base
        '''
        self.db_name = db_name
        self.users_table = 'TriveUsers'
        self.ips_table = 'TriveIps'
        self.conn = None
        self.cursor = None
        self.__create_db__()

    def __create_db__(self):
        '''

        :return: create a new database
        '''
        # connect to the data_base
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.__create_users_table__()
        self.__create_ips_table__()
        self.conn.commit()

    def __create_users_table__(self):
        '''

        :return: creates the users table if not exists
        '''
        users = F"CREATE TABLE IF NOT EXISTS {self.users_table} (Username TEXT, Email TEXT, Password TEXT)"
        self.cursor.execute(users)

    def __create_ips_table__(self):
        '''

        :return: creates the ips table if not exists
        '''
        ips = F"CREATE TABLE IF NOT EXISTS {self.ips_table} (Username TEXT, Ip TEXT)"
        self.cursor.execute(ips)

    def check_username_exist(self, username):
        '''

        :param username: username
        :return: check if the username is exist in the table
        '''
        sql = f"SELECT Username FROM {self.users_table} WHERE Username = '{username}'"
        self.cursor.execute(sql)
        return not (len(self.cursor.fetchall()) == 0)

    def add_user(self, username, email, password):
        '''

        :param username:
        :param email:
        :param password:
        :return: add the user to the table
        '''
        ret = False
        if not (self.check_username_exist(username)):
            ret = True
            sql = f"INSERT INTO {self.users_table} VALUES ('{username}','{email}','{password}')"
            self.cursor.execute(sql)
            self.conn.commit()
        return ret

    def change_password(self, username, password):
        '''

        :param username:
        :param password:
        :return: change the password for the username
        '''
        if self.check_username_exist(username):
            sql = f"UPDATE {self.users_table} set Password = '{password}' Where Username = '{username}'"
            self.cursor.execute(sql)
            self.conn.commit()
            return 'ok'
        return 'no'

    def change_email(self, username, new_email):
        '''

        :param username:
        :param newEmail:
        :return: change the email for the username
        '''
        if self.check_username_exist(username):
            sql = f"UPDATE {self.users_table} set Email = '{new_email}' Where Username = '{username}'"
            self.cursor.execute(sql)
            self.conn.commit()
            return 'ok'
        return 'no'

    def get_password_of_user(self, username):
        '''

        :param username:
        :return: password hash of username
        '''
        if self.check_username_exist(username):
            sql = f"SELECT Password from {self.users_table} WHERE Username == '{username}'"
            self.cursor.execute(sql)
            password = self.cursor.fetchall()
            return password[0][0]
        else:
            return

    def get_email_of_user(self, username):
        '''

        :param username:
        :return: email of username
        '''
        if self.check_username_exist(username):
            sql = f"SELECT Email from {self.users_table} WHERE Username == '{username}'"
            self.cursor.execute(sql)
            email = self.cursor.fetchall()
            return email[0][0]
        else:
            return

    def check_ip_exist_for_username(self, username, ip):
        '''

        :param username:
        :param ip:
        :return: "true" if the ip exists for "username" and false otherwise
        '''
        flag = False
        if self.check_username_exist(username):
            sql = f"SELECT Ip from {self.ips_table} WHERE Username == '{username}'"
            self.cursor.execute(sql)
            ips = self.cursor.fetchall()
            ip_list = []
            for tup in ips:
                ip_list.append(tup[0])
            flag = ip in ip_list
        return flag

    def add_ip_for_username(self, username, ip):
        '''

        :param username:
        :param ip:
        :return: add the ip to the username
        '''
        if not self.check_ip_exist_for_username(username, ip):
            sql = f"INSERT INTO {self.ips_table} VALUES ('{username}','{ip}')"
            self.cursor.execute(sql)
            self.conn.commit()

    def delete_ip_for_username(self, username, ip):
        '''

        :param username:
        :return: delete the user with username from the table
        '''
        ret = False
        # check that the username is in the table
        if self.check_username_exist(username):
            sql = f"DELETE from {self.ips_table} where Ip = '{ip}'"
            self.cursor.execute(sql)
            self.conn.commit()
            ret = True
        return ret
    
    def close_db(self):
        '''
        
        :return:close the data_base 
        '''
        pass