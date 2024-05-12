import select
import socket
import sys

from utils.utils import utfDecode

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

sys.argv
for arg in sys.argv:
    if "port" in arg:
        PORT = int(arg.split("=")[-1])
        print(PORT)
    if "ip" in arg:
        IP = arg.split(":")[-1]
    if "header_length" in arg:
        HEADER_LENGTH = int(arg.split(":")[-1])


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]

clients = {}

print(f"[ INFO ] Running server on {IP}:{PORT}...")


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            print("[ ERROR ] Empty Header")
            return False

        message_length = int(utfDecode(message_header).strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except Exception as e:
        print("[ ERROR ] ", e)
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(
                f"[ INFO ] Accepted new connection from {client_address[0]}:{client_address[1]} - username: {utfDecode(user['data'])}"
            )

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(
                    f"[ INFO ] Closed connection from {utfDecode(clients[notified_socket]['data'])}"
                )
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            print(f"{utfDecode(user['data'])} > {utfDecode(message['data'])}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(
                        user["header"]
                        + user["data"]
                        + message["header"]
                        + message["data"]
                    )

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
