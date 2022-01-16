import sqlite3


class DB:

    def __init__(self, db_name):
        '''

        :param db_name:
        '''
        self.db_name = db_name
        self.usersTable = 'TriveUsers'
        self.ipsTable = 'TriveIps'
        self.conn = None
        self.cursor = None
        self.createDB()

    def createDB(self):
        '''

        :return: create a new database
        '''
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.__create_users_table__()
        self.__create_ips_table__()

    def __create_users_table__(self):
        '''

        :return: creates the users table if not exists
        '''
        users = F"CREATE TABLE IF NOT EXISTS {self.usersTable} (Username TEXT, Email TEXT, Password TEXT)"
        self.cursor.execute(users)
        self.conn.commit()

    def __create_ips_table__(self):
        '''

        :return: creates the ips table if not exists
        '''
        ips = F"CREATE TABLE IF NOT EXISTS {self.ipsTable} (Username TEXT, Ip TEXT)"
        self.cursor.execute(ips)
        self.conn.commit()

    def check_username_exist(self, username):
        '''

        :param username: username
        :return: check if the username is exist in the table
        '''
        sql = f"SELECT Username FROM {self.usersTable} WHERE Username = '{username}'"
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
            sql = f"INSERT INTO {self.usersTable} VALUES ('{username}','{email}','{password}')"
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
            sql = f"UPDATE {self.usersTable} set Password = '{password}' Where Username = '{username}'"
            self.cursor.execute(sql)
            self.conn.commit()

    def change_email(self, username, newEmail):
        '''

        :param username:
        :param newEmail:
        :return: change the email for the username
        '''
        if self.check_username_exist(username):
            sql = f"UPDATE {self.usersTable} set Email = '{newEmail}' Where Username = '{username}'"
            self.cursor.execute(sql)
            self.conn.commit()

    def getPasswordOfUser(self, username):
        '''

        :param username:
        :return: password hash of username
        '''
        sql = f"SELECT Password from {self.usersTable} WHERE Username == '{username}'"
        self.cursor.execute(sql)
        password = self.cursor.fetchall()
        return password[0][0]

    def check_ip_exist_for_username(self, username, ip):
        '''

        :param username:
        :param ip:
        :return: "true" if the ip exists for "username" and false otherwise
        '''
        flag = False
        if self.check_username_exist(username):
            sql = f"SELECT Ip from {self.ipsTable} WHERE Username == '{username}'"
            self.cursor.execute(sql)
            ips = self.cursor.fetchall()
            ipList = []
            for tup in ips:
                ipList.append(tup[0])
            flag = ip in ipList
        return flag

    def add_ip_for_username(self, username, ip):
        '''

        :param username:
        :param ip:
        :return: add the ip to the username
        '''
        if not self.check_ip_exist_for_username(username, ip):
            sql = f"INSERT INTO {self.ipsTable} VALUES ('{username}','{ip}')"
            self.cursor.execute(sql)
            self.conn.commit()

    def delete_ip_for_username(self, username, ip):
        '''

        :param username:
        :return: delete the user with username from the table
        '''
        ret = False
        #check that the username is in the table
        if self.check_username_exist(username):
            sql = f"DELETE from {self.ipsTable} where Ip = '{ip}'"
            self.cursor.execute(sql)
            self.conn.commit()
            ret = True
        return ret

if __name__ == '__main__':
    myDB = DB('Trive')
    myDB.add_user('Tamir539', 'tamir.burstein@gmail.com', 'fdjighfduighgfd')
    print(myDB.check_username_exist('Tamir539'))
    myDB.add_ip_for_username('Tamir539', '1.1.1.1')


