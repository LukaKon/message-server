"""
    Script allows to manage user data like changing password.
"""

import argparse
import models
import clcrypto
# from utils.db_connection import DatabaseConnection as DB

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password (min 8 characters)')
# parser.add_argument(help='new name')  # TODO add possibility to change name
parser.add_argument('-n', '--new_pass', help='change password')
parser.add_argument('-l', '--list', help='list all users', action='store_true')
parser.add_argument('-d', '--delete', help='delete user', action='store_true')
parser.add_argument('-e', '--edit', help='edit user', action='store_true')
args = parser.parse_args()


def create_user(username, password):
    if len(password) < 8:
        print('Password is too short')
    else:
        models.Users(username, password).save_to_db()


def edit_user_data(username, password, new_pass):
    user = models.Users.load_user_by_username(username)
    if user:
        if clcrypto.check_password(password, user.hashed_password):
            if len(new_pass) < 8:
                print('Password is too short.')
            else:
                user.hashed_password = new_pass
        else:
            print('Password incorect.')
    else:
        print('User not yet in database')


def delete_user(username, password):
    user = models.Users.load_user_by_username(username)
    if clcrypto.check_password(password, user.hashed_password):
        user.delete()
    else:
        print('Incorrect password.')


def list_users():
    all_users = models.Users.load_all_users()
    for i in all_users:
        print(i.username)


if args.username and args.password and args.edit and args.new_pass:
    edit_user_data(args.username, args.password, args.new_pass)

elif args.username and args.password and args.delete:
    delete_user(args.username, args.password)

elif args.username and args.password:
    create_user(args.username, args.password)

elif args.list:
    list_users()

else:
    parser.print_help()

if __name__ == '__main__':
    pass
    # delete_user('andrzej')
