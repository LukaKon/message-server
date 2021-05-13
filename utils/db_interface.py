import utils.db_connection as DB


def interface(query: str, value):
    with DB.DatabaseConnection() as cursor:
        cursor.execute(query, value)
    re


if __name__ == '__main__':
    create_db()
    # users_table()
