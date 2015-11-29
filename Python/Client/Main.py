from Tkinter import *

import datetime
import os
import socket
import select
import threading

import aes
import basicencrypt


def AsciiArt(inputstring):
    """
    takes user input and converts allows user to paste ascii emojies quickly using special
    comands
    """
    files = [f for f in os.listdir("AsciiArt/") if f.endswith('.txt')]
    names2 = list()
    for file in files:
        h = "!"+file
        names2.append (h.replace(".txt", ""))
    if inputstring == "!help":
        names = list()
        for file in files:
            names.append (file.replace("AsciiArt/", "").replace(".txt", ""))
        print_("Valid Picture Commands are:", False)
        for file in names:
            print_(file, False)
    elif inputstring in names2:
        file = inputstring.replace("!", "")
        filepath = "AsciiArt/" + file + ".txt"
        output = open(filepath, 'r').read()
        server_socket.send(output)
    else:
        print_("This is not a valid command! Try '!help'", False)


def create_alias(server_socket):
    """
    Sends a request to the sever asking if the requested alias has been taken
    if not it is assigned and this ends otherwise will loop till new alias is taken
    """
    requested_alias = ""
    while True:
        if not requested_alias:
            requested_alias = Alias_entr.get()
            server_socket.send(requested_alias)
        else:
            server_decision = server_socket.recv(4096)
            if server_decision == "Accepted":
                return print_("Alias Accepted", False)
            elif server_decision == "Rejected":
                requested_alias = ""
                return print_("Alias Rejected", False)


def sel():
    """
    whenever one of the radio buttons is pressed the global variable controlling
    the type of encryption used is assigned
    """
    global encryption_selected
    if var.get() == 0:
        encryption_selected = ""
    elif var.get() == 1:
        encryption_selected = "basic"
    elif var.get() == 2:
        encryption_selected = "aes"


def Main_GUI():
    """
    Creates the GUI for the client
    """
    global entr, text1, root, ip_entr, port_entr, Alias_entr, var
    root = Tk()
    root.title('Chat Client')
    Button(root, text='Send', command=send).pack(side= BOTTOM)
    entr = Entry(root)
    entr.pack(side=BOTTOM, fill=X)
    entr.focus()
    entr.bind('<Return>', (lambda event: send()))
    text1 = Text(root, relief = SUNKEN)
    scr = Scrollbar(root)
    text1.config(state=DISABLED, yscrollcommand=scr.set)
    text1.pack(side= LEFT, fill =BOTH)
    scr.config(command=text1.yview)
    scr.pack(side=LEFT, fill=Y)

    seperator = Frame(root)
    seperator.pack(side=LEFT)
    Alias = Label(seperator, text='Alias')
    Alias.grid(row=0, column=0)
    Alias_entr =Entry(seperator)
    Alias_entr.grid(row=0, column=1)
    ip = Label(seperator, text='IP')
    ip.grid(row=1, column=0)
    ip_entr =Entry(seperator)
    ip_entr.grid(row=1, column=1)
    ip_entr.insert(END, '10.89.217.194')
    ip_entr.focus()
    port = Label(seperator, text='Port')
    port.grid(row=2, column=0)
    port_entr = Entry(seperator)
    port_entr.grid(row=2, column=1)
    port_entr.insert(END, '8421')
    Button(seperator, text='Connect', command=main).grid(row=3, column=1)
    var = IntVar()
    radio0 = Radiobutton(seperator, text="No encryption", variable=var, value=0,
                         command=sel)
    radio0.grid(row=4, column=1)
    radio1 = Radiobutton(seperator, text="Basic encryption", variable=var, value=1,
                         command=sel)
    radio1.grid(row=5, column=1)
    radio2 = Radiobutton(seperator, text="AES encryption", variable=var, value=2,
                         command=sel)
    radio2.grid(row=6, column=1)
    port_entr.focus()
    root.mainloop()


def main():
    """
    assigns the default value for the type of encryption used for messages
    starts the thread that runs the clients connection to the server
    """
    global encryption_selected
    encryption_selected = ""
    server_running_thread = threading.Thread(target=server)
    server_running_thread.daemon = True
    server_running_thread.start()


def print_(data, incoming_message):
    """
    will read if there is and incoming message check for its encryption type
    if its a message it is then decrypted if it needs it and is output to the text box
    """
    global line11
    if (len(data) > 0) and (incoming_message == False):
        # if it is not a message that needs to be output to the text box
        data = data + '\n'
    elif incoming_message:
        # the size alias part of the string is found
        count = 0
        for char in data:
            if char == ' ':
                count += 1
                break
            else:
                count += 1
        if data[-10:] == "rbUb7qe14x":
            # if the identifier above is found on the end of the message then
            # data has the alias put in front with the main message decrypted using basicencrypt module
            data = data[:count] + basicencrypt.decrypt(data[count:-10]) + '\n'
        elif data[-1:] == "]":
            # if a ']' is at the end of the message then the message has the
            # alias and original length parts taken off the front and is then converted to an
            # integer list to be decrypted
            extracted_data = data[count:]
            extracted_data = extracted_data.split(',')
            ori_length = int(extracted_data[0])
            data_list = []
            for i in range(1, len(extracted_data)):
                if i != len(extracted_data):
                    temp = extracted_data[1]
                    temp = temp[1:]
                    data_list.append(int(temp))
                else:
                    temp = extracted_data[i]
                    temp = temp[1:-1]
                    data_list.append(int(temp))
            decrypt = aes.AESModeOfOperation()
            key = get_aes_key()
            mode = decrypt.modeOfOperation["OFB"]
            decrypted = decrypt.decrypt(data_list,ori_length,mode, key,
                       decrypt.aes.keySize["SIZE_128"],
                       [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92])
            # the decrypted message is then output to a string with the alias at the front
            data = data[:count] + decrypted + '\n'
        else:
            data = data + '\n'
    # writes data to the text box
    line11 += 1.0
    text1.config(state=NORMAL)
    text1.insert(line11, data)
    text1.mark_set(INSERT, line11)
    text1.config(state=DISABLED)


def get_aes_key():
    current_datetime = str(datetime.datetime.now())
    key = []
    for char in current_datetime:
        key.append(ord(char))
        if len(key) == 16:
            break
    return key

def send():
    """
    will take a message and encypt it based on the setting chosen in encryption_selected
    """
    global stext
    global encryption_selected
    stext = entr.get()
    entr.delete(0, END)
    if encryption_selected == "basic":
        # Takes the message to be sent and encrypts it using the basicencrypt module
        stext = basicencrypt.encrypt(stext)
        # Adds identifier onto the end of the message
        stext += "rbUb7qe14x"
        server_socket.send(stext)
    elif encryption_selected == "aes":
        # Takes the message to be sent and encrypts it using the aes module
        encrypt = aes.AESModeOfOperation()
        key = get_aes_key()
        mode, orig_len, ciphertext = encrypt.encrypt(stext, encrypt.modeOfOperation["OFB"], key,
                                         encrypt.aes.keySize["SIZE_128"],
                                         [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92])
        # converts the integer list that is output to a string
        ciphertext = str(ciphertext)
        # the original message length is then appended to the front of the message
        ciphertext = str(orig_len) + "," + ciphertext
        server_socket.send(ciphertext)
    else:
        # if there is no encryption the message is just sent
        server_socket.send(stext)


def server():
    """
    creates and maintains the connection to the server as well as handling what should
    happen with any new messages that the client recieves from the server
    """
    global server_socket
    # Gets the ip and port from the input boxes
    host = ip_entr.get()
    port = int(port_entr.get())
    # creates the socket to connect to the server on and the connects
    server_socket = socket.socket()
    server_socket.settimeout(2)
    server_socket.connect((host, port))
    print_(("Connected to remote host." + str(datetime.date.today())), False)
    create_alias(server_socket)
    print_("You can now send messages.", False)
    while True:
        socket_list = [sys.stdin, server_socket]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for current_socket in read_sockets:
            if current_socket == server_socket:
                # incoming message
                data = current_socket.recv(4096)
                if not data:
                    print_("Disconnected from chat server", False)
                    server_socket.close()
                    sys.exit()
                else:
                    print_(data, True)
            else:
                #message to be sent from client
                server_socket.send(stext)


line11 = 1
if __name__ == "__main__":
    Main_GUI()
