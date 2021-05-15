import psycopg2
import utils.db_login as login


class MyConnectionFailed(Exception):
    pass


class DatabaseConnection:
    def __init__(self):
        self.host = login.host
        # self.database = 'ahglgelvb'
        self.database = login.database
        self.user = login.user
        self.password = login.password
        # self.password = '9642398'
        self.port = login.port
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port)
            self.cursor = self.connection.cursor()
            return self.cursor
        except psycopg2.OperationalError:
            raise MyConnectionFailed('No conected')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()


if __name__ == '__main__':
    conn = DatabaseConnection()
    conn.__enter__()
