import select
import socket
import string
import sys


def prompt():
    sys.stdout.write("You - ")
    sys.stdout.flush()


def main():
    host = "192.168.133.129"
    port = 8421
     
    server_socket = socket.socket()
    server_socket.settimeout(2)
    server_socket.connect((host, port))
     
    print("Connected to remote host. You can now send messages")
    prompt()
     
    while True:
        socket_list = [sys.stdin, server_socket]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for current_socket in read_sockets:
            if current_socket == server_socket:
                data = current_socket.recv(4096)
                if not data:
                    print("Disconnected from chat server")
                    server_socket.close()
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    prompt()
            else:
                msg = sys.stdin.readline()
                server_socket.send(msg)
                prompt()

if __name__ == "__main__":
    main()
