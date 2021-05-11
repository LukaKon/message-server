import psycopg2
# import os
import subprocess
import db_login as login

DB_NAME = 'message_server'


class DatabaseConnection:
    def __init__(self):
        # subprocess.run()    # TODO execute command from below

        # "SELECT 'CREATE DATABASE message-server' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'message-server')\gexec"
        self.host = login.host
        self.database = DB_NAME
        self.user = login.user
        self.password = login.password
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
            print('not connected')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()


if __name__ == '__main__':
    conn = DatabaseConnection()
    conn.__enter__()
