from db_connection import DatabaseConnection

# class DBinterface:
#     def __init__(self):
#         self.create_db()
#         self.create_users_table()


#     def create_db(self):
#         # SELECT 'CREATE DATABASE <your db name>' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '<your db name>')\gexec
#        with dbconn.

#     def create_users_table(self) -> None:

# sql_db = "SELECT 'CREATE DATABASE message-server' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'message-server')\gexec"
sql_db = "CREATE DATABASE message_server;"
sql_users = """
            CREATE TABLE users (
                id serial PRIMARY KEY,
                usernamme varchar(255),
                hashhed_password varchar(80)
            );
            """


def create_db():
    with DatabaseConnection() as dbconn:
        dbconn.execute(sql_db)
        # print(dbconn)


def users_table():
    with DatabaseConnection() as dbconn:
        dbconn.execute(sql_users)


if __name__ == '__main__':
    create_db()
    # users_table()
