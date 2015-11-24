from Tkinter import * 
import select
import socket
import string
import sys
import threading


def Main_GUI():
    global entr, text1, root, ip_entr, port_entr
    root=Tk()
    root.title('Chat Client')
    Button(root, text='Send', command=send).pack(side= BOTTOM)
    entr =Entry(root)
    entr.pack(side=BOTTOM, fill=X)
    entr.focus()
    entr.bind('<Return>', (lambda event: send()))
    text1 =Text(root, relief = SUNKEN)
    scr =Scrollbar(root)
    text1.config(state=DISABLED, yscrollcommand=scr.set)
    text1.pack(side= LEFT, fill =BOTH)
    scr.config(command=text1.yview)
    scr.pack(side=LEFT, fill=Y)

    seperator= Frame(root)
    seperator.pack(side=LEFT)
    ip =Label(seperator, text='IP')
    ip.grid(row=0, column=0)
    ip_entr =Entry(seperator)
    ip_entr.grid(row=0, column=1)
    ip_entr.insert(END, '192.168.17.129')
    ip_entr.focus()
    port =Label(seperator, text='Port')
    port.grid(row=1, column=0)
    port_entr =Entry(seperator)
    port_entr.grid(row=1, column=1)
    port_entr.insert(END, '8421')
    Button(seperator, text='Connect', command=main).grid(row=2, column=1)
    port_entr.focus()
    root.mainloop()
    

def send():
    global stext
    stext= entr.get()
    entr.delete(0, END)
    print_(stext)
    try:
        server_socket.send(stext)
    except:
        print_("Problem while sending text...")


def print_(data):
    global line11
    if len(data) > 0:
        data= data + '\n'
    line11 +=1.0
    text1.config(state=NORMAL)
    text1.insert(line11, data)
    text1.mark_set(INSERT, line11)
    text1.config(state=DISABLED)



def AsciiArt (inputstring):
    """takes user input and converts allows user to paste ascii emojies quickly using special
    comands"""
    import os
    files = [f for f in os.listdir("AsciiArt/") if f.endswith('.txt')]
    names2 = list()
    for file in files:
        h = "!"+file
        names2.append (h.replace(".txt", ""))
    if inputstring == "!help":
        names = list()
        for file in files:
            names.append (file.replace("AsciiArt/", "").replace(".txt", ""))
        print_("Valid Picture Commands are:")
        for file in names:
            print_(file)
    elif inputstring in names2:
        file = inputstring.replace("!", "")
        filepath = "AsciiArt/" + file + ".txt"
        output = open(filepath, 'r').read()
        server_socket.send(output)
    else:
        print_("This is not a valid command! Try '!help'")


def main():
    Server_Running_thread =threading.Thread(target=Server)
    Server_Running_thread.start()


def create_alias(server_socket):
    requested_alias = ""
    while True:
        if not requested_alias:
            requested_alias = "its not broke"
            server_socket.send(requested_alias)
        else:
            server_decision = server_socket.recv(4096)
            if server_decision == "Accepted":
                return
            elif server_decision == "Rejected":
                requested_alias = ""

    
def Server():
    global server_socket
    host = ip_entr.get()
    port = int(port_entr.get())

    server_socket = socket.socket()
    server_socket.settimeout(2)
    server_socket.connect((host, port))
    print_("Connected to remote host.")
    create_alias(server_socket)
    print_("You can now send messages.")

    while True:
        socket_list = [sys.stdin, server_socket]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for current_socket in read_sockets:
            if current_socket == server_socket:
                data = current_socket.recv(4096)
                if not data:
                    print_("Disconnected from chat server")
                    server_socket.close()
                    sys.exit()
                else:
                    print_(data)

            else:
                server_socket.send(stext)

line11=1
if __name__ == "__main__":
    Main_GUI()
