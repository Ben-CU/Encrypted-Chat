import sys


def create_alias(current_socket, alias_dict):
    while True:
        requested_alias = current_socket.recv(4096)
        if requested_alias and (requested_alias in alias_dict):
            current_socket.send("Rejected")
        elif requested_alias:
            alias_dict[current_socket] = requested_alias
            current_socket.send("Accepted")
            return


def send_message(sending_socket, message, connection_list, alias_dict, server_socket):
    """
    function to pass the message from one client onto all of the others apart from the server and the sending
    socket
    :param sending_socket: the socket that the client with the message sent from
    :param message: the message from on client to all of the others
    """
    message_for_sender = "You: " + message
    message_for_all = alias_dict.get(sending_socket) + ": " + message
    print(message)
    for current_socket in connection_list:
        if (current_socket != server_socket) and (current_socket != sending_socket):
            try:
                current_socket.send(message_for_all)
            except:
                print("Client with alias: " + alias_dict.get(current_socket) + " has disconnected, alias now available")
                del alias_dict[current_socket]
                connection_list.remove(current_socket)
        elif current_socket == sending_socket:
            current_socket.send(message_for_sender)
    return

if __name__ == "__main__":
    print("This module is not meant to be run on its own")
    sys.exit()
