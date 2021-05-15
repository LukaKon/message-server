import argparse
import models
import clcrypto

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password (min 8 characters)')
parser.add_argument('-t', '--to', help='to who message will be sent')
parser.add_argument('-s', '--send', help='message text')
parser.add_argument(
    '-l', '--list', help='list all messages', action='store_true')
args = parser.parse_args()


def check_user_and_pass(username, password):
    user = models.Users.load_user_by_username(username)
    if user:
        if clcrypto.check_password(password, user.hashed_password):
            return True
        else:
            print(f'Password is incorrect.')
            return False
    else:
        print(f'User "{username}" does not exist.')
        return False


# def list_messages(username, password):
#     user = models.Users.load_user_by_username(username)
#     if user:
#         if clcrypto.check_password(password, user.hashed_password):
#             all_messages = models.Messages.load_all_messages(user.id)
#             for message in all_messages:
#                 target_user = models.Users.load_user_by_id(message.to_id)
#                 print(
#                     f'Sent to: {target_user.username} message: {message.message} in {message.creation_date}')
#         else:
#             print(f'Password is incorrect.')
#     else:
#         print(f'User "{username}" does not exist.')
def list_messages(username, password):
    if check_user_and_pass(username, password):
        user = models.Users.load_user_by_username(username)
        all_messages = models.Messages.load_all_messages(user.id)
        for message in all_messages:
            target_user = models.Users.load_user_by_id(message.to_id)
            print(
                f'Sent to: {target_user.username} message: {message.message} in {message.creation_date}')


# def messag(username, password):
#     user = models.Users.load_user_by_username(username)
#     all_messages = models.Messages.load_all_messages(user.id)
#     if check_user_and_pass(username, password):
#         friends = []
#         other_user = 0
#         friend_names = {}
#         key = 1
#         for message in all_messages:
#             if message.from_id != user.id:
#                 other_user = message.from_id
#             elif message.to_id != user.id:
#                 other_user = message.to_id
#             if other_user in friends:
#                 friends.append(other_user)
#         for friend in friends:
#             helper = models.Users.load_user_by_id(friend)
#             friend_names[key] = helper.username
#             key += 1
#         for x in friend_names:
#             print(f'{x}: {friend_names[x]}')
#         try:
#             user_selection = int(input('Select archive: '))

# def receive_messages(username, password, sender):
#     user = models.Users.load_user_by_username(username)
#     sender = models.Users.load_user_by_username(sender)
#     if check_user_and_pass(username, password):
#         if sender and user:
#             all_messages = models.Messages.load_all_messages(
#                 user.id, sender.id)
#             for message in all_messages:
#                 # target_user = models.Users.load_user_by_id(message.to_id)
#                 print(
#                     f'From: {sender.username} message: {message.message} in {message.creation_date}')
#         else:
#             print(f'Sender "{sender}" not exist.')


def sent_message(username, password, addressee, message):
    sender = models.Users.load_user_by_username(username)
    if check_user_and_pass(username, password):
        addr = models.Users.load_user_by_username(addressee)
        if addr:
            if len(message) < 255:
                mess = models.Messages(sender.id, addr.id, message)
                mess.save_to_db()
            else:
                print('Message is to long.')
        else:
            print(f'Addressee "{addressee}" not exist.')


if args.username and args.password and args.to and args.send:
    sent_message(args.username, args.password, args.to, args.send)

elif args.username and args.password and args.list:
    list_messages(args.username, args.password)

else:
    parser.print_help()
