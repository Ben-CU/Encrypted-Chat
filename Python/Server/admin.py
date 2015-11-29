import sys


def shutdown(connection_list, server_socket):
    print("Disconnecting clients")
    for current_socket in connection_list:
        if current_socket != server_socket:
            current_socket.send("You have been disconnected - Server Shutting Down\n")
            current_socket.close()
    print("Disconnecting server")
    server_socket.close()
    print("Server has shutdown - Will now exit")


if __name__ == "__main__":
    print("This module is not meant to be run on its own")
    sys.exit()
