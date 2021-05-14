from os import truncate
import sys
import subprocess

import psycopg2
try:
    import colorama
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorama'])
from colorama import init, Fore
import clcrypto as ps
import utils.db_connection as DB

init(autoreset=True)


class Users:
    """
    Class that handle users.
    """

    def __init__(self, username: str = '', password: str = '', salt: str = '') -> None:
        self._id = -1
        self.username = username
        self._hashed_password = ps.hash_password(password, salt)

    def __str__(self) -> str:
        return f'User: {self.username} with id: {self._id} and password: {self._hashed_password}.'

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password: str, salt: str = ''):
        self._hashed_password = ps.hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password: str):
        self.set_password(password)

    def save_to_db(self):
        if self._id == -1:
            # users_query = """SELECT users.username FROM users"""
            # with DB.DatabaseConnection() as cursor:
            #     cursor.execute(users_query)
            #     all_names = [row[0] for row in cursor.fetchall()]
            # checking if user exist in database is not necesary because 'else' will update record?
            # TODO create update method separatly... why?

            # if self.username not in all_names:
            query = """INSERT INTO users(username,hashed_password) VALUES (%s,%s) RETURNING id"""
            values = (self.username, self.hashed_password)
            try:
                with DB.DatabaseConnection() as cursor:
                    cursor.execute(query, values)
                    self._id = cursor.fetchone()[0]  # ['id']
                    print(f'{Fore.LIGHTGREEN_EX}User added. Your id: {self._id}')
                return True
            except psycopg2.errors.UniqueViolation:
                print(f'{Fore.LIGHTRED_EX}User "{self.username}" already exist.')

        else:
            query = """UPDATE users SET username=%s, hashed_password=%s WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            with DB.DatabaseConnection() as cursor:
                cursor.execute(query, values)
            print(f'{Fore.LIGHTGREEN_EX}User datas are updated.')
            return True

    def delete(self):
        query = """DELETE FROM users WHERE id=%s"""
        with DB.DatabaseConnection() as cursor:
            cursor.execute(query, (self.id,))
        self._id = -1
        print(f'{Fore.LIGHTBLUE_EX}User "{self.username}" is deleted.')
        return True

    @staticmethod
    def load_user_by_username(username: str):
        query = """SELECT users.id, users.username, users.hashed_password FROM users WHERE username=%s"""
        values = username,
        with DB.DatabaseConnection() as cursor:
            cursor.execute(query, values)
            data = cursor.fetchone()
            if data:
                id_, username, hashed_password = data
                loaded_user = Users(username)
                loaded_user._id = id_
                loaded_user._hashed_password = hashed_password
                return loaded_user
            else:
                return None

    @staticmethod
    def load_user_by_id(id_: int):
        query = """SELECT users.id, users.username, users.hashed_password FROM users WHERE id=%s"""
        values = id_,
        with DB.DatabaseConnection() as cursor:
            cursor.execute(query, values)
            data = cursor.fetchone()
            if data:
                id_, username, hashed_password = data
                loaded_user = Users(username)
                loaded_user._id = id_
                loaded_user._hashed_password = hashed_password
                return loaded_user
            else:
                return None

    @staticmethod
    def load_all_users():
        query = """SELECT users.id, users.username, users.hashed_password FROM users ORDER BY id"""
        with DB.DatabaseConnection() as cursor:
            cursor.execute(query)
            users = []
            for row in cursor.fetchall():
                id_, username, hashed_password = row
                loaded_user = Users(username)
                loaded_user._id = id_
                loaded_user._hashed_password = hashed_password
                users.append(loaded_user)
            return users


class Messages:
    """Class that handle messages"""

    def __init__(self, from_id: int, to_id: int, message: str) -> None:
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.message = message
        self._creation_date = None

    def __str__(self):
        return f'Message from {self.from_id} to {self.to_id}: {self.message}.'

    @property
    def id(self):
        return self._id

    @property
    def creation_date(self):
        return self._creation_date

    def save_to_db(self):
        if self._id == -1:
            query = """INSERT INTO messages(from_id, to_id, message) VALUES (%s,%s,%s) RETURNING id, creation_date"""
            values = (self.from_id, self.to_id, self.message)
            with DB.DatabaseConnection() as cursor:
                cursor.execute(query, values)
                self._id, self._creation_date = cursor.fetchone()  # ['id']
                print(
                    f'{Fore.LIGHTGREEN_EX}Message added {self._creation_date}. message id: {self._id}')
            return True

    def delete(self):
        query = """DELETE FROM messages WHERE id=%s"""
        with DB.DatabaseConnection() as cursor:
            cursor.execute(query, (self.id,))
        self._id = -1
        return True

    # def messages_user_sent(self):
    #     if self._id != 1:
    #         query = '''SELECT DISTINCT ON (messages.id) users.username, users.id , messages.message, messages.creation_date
    #         FROM users
    #         JOIN messages ON users.id=messages.from_id
    #         WHERE users.id=1'''
    #         values = self._id,
    #         with DB.DatabaseConnection() as cursor:
    #             cursor.execute(query, values)

    @staticmethod
    def load_all_messages():
        query = """SELECT id, from_id, to_id, message, creation_date FROM messages"""
        messages = []
        with DB.DatabaseConnection() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                id_, from_id, to_id, message, creation_date = row
                loaded_message = Messages(from_id, to_id, message)
                loaded_message._id = id_
                loaded_message._creation_date = creation_date
                messages.append(loaded_message)
        return messages


if __name__ == '__main__':
    us = Users('Jan Kowalski', '123456')
    em = Users('Anna Zabawa', 'koala123')
    pe = Users('Ewa123', '8924')
    ne = Users('Adam34')
    na = Users('Adam34')
    us.save_to_db()
    em.save_to_db()
    pe.save_to_db()
    ne.save_to_db()
    na.save_to_db()

    print(Users.load_user_by_username('Jan Kowalski'))
    print(Users.load_user_by_id(2))
    print('-------------')
    for i in Users.load_all_users():
        print(i)
    # print(Users.load_all_users())

    me_1 = Messages(1, 2, 'new message')
    me_2 = Messages(3, 1, 'Something new')
    me_3 = Messages(2, 3, 'Wiadomości')
    me_4 = Messages(1, 3, 'To Ci mówię... bla bla bla')
    me_5 = Messages(1, 3, 'To Ci odpowiadam...')
    me_1.save_to_db()
    me_2.save_to_db()
    me_3.save_to_db()
    me_4.save_to_db()
    me_5.save_to_db()

    for i in Messages.load_all_messages():
        print(i)

    na.delete()
