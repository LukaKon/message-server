import sys
import subprocess
try:
    import colorama
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorama'])
from colorama import init, Fore
import psycopg2
# from psycopg2 import extensions
import utils.db_login as log
# from utils.db_connection import DatabaseConnection as DB
# import utils.db_connection as DB
init(autoreset=True)
# from psycopg2 import errors

USER = log.user
HOST = log.host
PASSWORD = log.password
PORT = log.port
DB_NAME = 'message_server'

db = f"CREATE DATABASE {DB_NAME};"
users_tab = """
                CREATE TABLE public.users (
                    id serial NOT NULL,
                    username varchar(255) NOT NULL UNIQUE,
                    hashed_password varchar(80),
                    PRIMARY KEY (id)
                );
                """
messages_tab = """
                CREATE TABLE public.messages (
                    id serial NOT NULL,
                    from_id int NOT NULL,
                    to_id int NOT NULL,
                    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0),
                    message text,
                    PRIMARY KEY (id),
                    FOREIGN KEY (from_id) REFERENCES users(id),
                    FOREIGN KEY (to_id) REFERENCES users(id)
                );
                """


def create_db():
    """
    Create database.
    """
    conn = psycopg2.connect(user=USER, password=PASSWORD,
                            host=HOST, port=PORT)
    conn.autocommit = True

    try:
        with conn.cursor() as cursor:
            cursor.execute(db)

    except psycopg2.errors.DuplicateDatabase:
        print(f'{Fore.YELLOW}Database "{DB_NAME}" already exist.')
    else:
        print(f'{Fore.GREEN}Database "{DB_NAME}" created.')
    finally:
        conn.close()


def create_table(sql_code, db=DB_NAME):
    """
    Create table in database.

    :param str sql_code: sql code to run
    :param str db: name of db,
    """
    conn = psycopg2.connect(user=USER, password=PASSWORD,
                            host=HOST, database=db, port=PORT)
    conn.autocommit = True
    table_name = sql_code.split()[2]
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_code)

    except psycopg2.errors.DuplicateTable:
        print(f'{Fore.YELLOW}Table "{table_name}" already exist.')
    else:
        print(f'{Fore.GREEN}Table \"{table_name}\" created.')

    finally:
        conn.close()


if __name__ == '__main__':
    create_db()
    # for query in sql_tab:
    # create_table(query)
    # create_table(sql_tab[0])
    # create_table(sql_tab[1])
    create_table(users_tab, DB_NAME)
    create_table(messages_tab)
    # cr_db()
