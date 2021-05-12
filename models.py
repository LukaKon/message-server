import itertools
import password as ps
import utils.db_connection as DB


class Users:
    """
    Class to handle users.
    """
    next_id = itertools.count(1)

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
            query = """INSERT INTO users(username,hashed_password) VALUES (%s,%s) RETURNING id"""
            values = (self.username, self.hashed_password)
            with DB.DatabaseConnection() as cursor:
                cursor.execute(query, values)
                self._id = cursor.fetchone()[0]  # ['id']
                print(self._id)
            return True
        else:
            return False

    def delete(self):
        self.id = -1

    @staticmethod
    def load_user_by_username(self):
        pass

    @staticmethod
    def load_user_by_id(self):
        pass

    @staticmethod
    def load_all_users(self):
        pass


class Messages:
    def __init__(self) -> None:
        self.id = -1
        self.from_id
        self.to_id
        self.text
        self.creation_data = None

    def save_to_db(self):
        pass

    def load_all_messages(self):
        pass


if __name__ == '__main__':
    us = Users('Jan Kowalski', '123456')
    us.save_to_db()
