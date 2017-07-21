import select
import socket
import sys
import threading
import urllib

import admin
import client

connection_list = []
alias_dict = {}


def client_listening(server_socket):
    """
    Reads incoming data from clients, if it is a new client the connection socket is added
    to the connection list otherwise the data is sent to all the other clients as a message
    """
    while True:
        read_sockets, write_sockets, error_sockets = select.select(connection_list, [], [])
        for current_socket in read_sockets:
            if current_socket == server_socket:
                new_socket, new_address = server_socket.accept()
                connection_list.append(new_socket)
                create_alias_thread = threading.Thread(target=client.create_alias, args=(new_socket, alias_dict, ))
                create_alias_thread.daemon = True
                create_alias_thread.run()
                print("Client with alias " + alias_dict.get(new_socket))
            else:
                new_message = current_socket.recv(4096)
                if new_message and (new_message != "/"):
                    send_message_thread = threading.Thread(target=client.send_message, args=(current_socket,
                                                                                             new_message,
                                                                                             connection_list,
                                                                                             alias_dict,
                                                                                             server_socket))
                    send_message_thread.daemon = True
                    send_message_thread.run()



def get_host_ip():
    """
    Gets the IP for the server and if the server is to be running on a LAN or not
    if the sever is not running on a LAN then the ip is produced automatically
    """
    sys.stdout.write("Is this a LAN server? ( y/n ) ")
    user_input = sys.stdin.readline()
    if (user_input[0] == "y") or (user_input[0] == "Y"):
        ip = get_local_ip()
        return ip
    elif (user_input[0] == "n") or (user_input[0] == "N"):
        ip = urllib.urlopen("http://simplesniff.com/ip").read()
        ip = str(ip[:-1])
        return ip
    else:
        print("That is not a valid input please try again")
        get_host_ip()


def get_local_ip():
    sys.stdout.write("Are you connected to the internet? ( y/n ) ")
    user_input = sys.stdin.readline()
    if (user_input[0] == "y") or (user_input[0] == "Y"):
        ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_socket.connect(("8.8.8.8", 0))
        ip = ip_socket.getsockname()[0]
        ip_socket.close()
        return ip
    elif (user_input[0] == "n") or (user_input[0] == "N"):
        sys.stdout.write("Please enter you local ip: ")
        user_input = sys.stdin.readline()
        ip = str(user_input)[:-1]
        return ip
    else:
        print("That is not a valid input please try again")
        get_local_ip()


def get_port():
    sys.stdout.write("What port would you like to use? ")
    user_input = sys.stdin.readline()
    return int(user_input)


def main(restart=False, host_ip="", port=0):
    if not restart:
        host_ip = get_host_ip()
        port = get_port()

    server_socket = socket.socket()
    server_socket.bind((host_ip, port))
    server_socket.listen(20)
    connection_list.append(server_socket)
    alias_dict[server_socket] = "Server"

    print("")
    print("The server has been started")
    print("IP: " + host_ip)
    print("Port: " + str(port))

    client_listening_thread = threading.Thread(target=client_listening, args=(server_socket, ))
    client_listening_thread.daemon = True
    client_listening_thread.start()

    while True:
        user_input = sys.stdin.readline()
        user_input = str(user_input)[:-1]
        if user_input == "shutdown":
            admin.shutdown(connection_list, server_socket)
            sys.exit()


if __name__ == "__main__":
    main()
