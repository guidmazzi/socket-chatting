import socket

from utils.utils import utfEncode

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

print(f"[ INFO ] Connected to {IP}:{PORT}")

username = utfEncode(my_username)
username_header = utfEncode(f"{len(username) :< {HEADER_LENGTH}}")
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")

    if message:
        message = utfEncode(message)
        message_header = utfEncode(f"{len(message) :< {HEADER_LENGTH}}")
        client_socket.send(message_header + message)
