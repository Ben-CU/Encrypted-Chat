import select
import socket
import sys
import threading

connection_list = []
server_socket = socket.socket()
global server_command


def client_handler():
    """
    Reads incoming data from clients, if it is a new client the connection socket is added
    to the connection list otherwise the data is sent to all the other clients as a message
    """
    while True:
        # The list of sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(connection_list, [], [])

        for current_socket in read_sockets:
            if current_socket == server_socket:
                # A new client connects to the server
                new_socket, client_address = server_socket.accept()
                connection_list.append(new_socket)
                print("Client from " + str(client_address) + " has connected")
            else:
                # A client has sent a message
                new_message = current_socket.recv(4096)
                if new_message:
                    sys.stdout.write(str(current_socket) + " " + new_message)
                    send_message(current_socket, new_message)


def get_host_ip():
    """
    Not Currently working properly
    Gets the IP for the server and if the server is to be running on a LAN or not
    """
    sys.stdout.write("Is this a LAN server ( y/n ): ")
    user_input = sys.stdin.readline()
    if (user_input[0] == "y") or (user_input[0] == "Y"):
        # runs the command ifconfig and takes the
        import os
        local_ip = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
        return local_ip.read()
    elif (user_input[0] == "n") or (user_input[0] == "N"):
        import urllib
        ip = urllib.urlopen('http://simplesniff.com/ip').read()
        ip = str(ip[0:-1])
        return ip
    else:
        print("That is not a valid choice, please try again")
        get_host_ip()


def send_message(sending_socket, message):
    """
    function to pass the message from one client onto all of the others apart from the server and the sending
    socket
    :param sending_socket: the socket that the client with the message sent from
    :param message: the message from on client to all of the others
    """
    for current_socket in connection_list:
        if (current_socket != server_socket) and (current_socket != sending_socket):
            current_socket.send(message)


def read_server_commands():
    """
    Reads input to the server via a user and will write that to the global variable server_command
    """
    global server_command
    while True:
        server_command = sys.stdin.readline()
        server_command = str(server_command)[0:-1]


def server_shutdown():
    """
    Shuts down the server by closing all the client sockets then the server socket
    after that the program exits
    """
    print("Disconnecting clients")
    # closes the clients socket and tells them what is happening
    for current_socket in connection_list:
        if current_socket != server_socket:
            current_socket.send("You have been disconnected - Server Shutting Down\n")
            current_socket.close()
    print("Disconnecting server")
    # closes the servers socket then exits the program
    server_socket.close()
    sys.exit()


def main():
    """
    The main function that sets up the server with its socket and starts the threads which the server
    runs on.
    """
    # defines the ip and port for the server to run on
    host_ip = "192.168.133.129"
    port = 8421

    # creates the servers socket and sets it to listen
    server_socket.bind((host_ip, port))
    server_socket.listen(20)
    connection_list.append(server_socket)

    print("The server has been started on")
    sys.stdout.write("Host: " + host_ip)
    print("Port: " + str(port))

    # creates and starts the thread to handle input to the server
    read_command_thread = threading.Thread(target=read_server_commands)
    read_command_thread.daemon = True
    read_command_thread.start()

    # creates and starts the thread to handle incoming connections and messages
    client_handling_thread = threading.Thread(target=client_handler)
    client_handling_thread.daemon = True
    client_handling_thread.start()

    # handles commands being passed by server_command
    while True:
        if server_command == "shutdown":
            server_shutdown()

if __name__ == "__main__":
    server_command = ""
    main()
