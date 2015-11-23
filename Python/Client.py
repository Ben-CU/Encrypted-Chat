from Tkinter import * 
import select
import socket
import string
import sys
import threading
import time

def Main_GUI():
    global entr, text1, rootM
    rootM=Tk()
    rootM.title=('Chat Client')
    Button(rootM, text='Send', command=send).pack(side = BOTTOM)
    entr =Entry(rootM)
    entr.pack(side=BOTTOM, fill=X)
    entr.focus()
    entr.bind('<Return>', (lambda event: send()))
    text1 =Text(rootM, relief = SUNKEN)
    text1.config(state=DISABLED)
    text1.pack(side= LEFT, fill = BOTH)
    rootM.mainloop()
    

def send():
    global stext
    stext= entr.get()
    entr.delete(0, END)
    if stext[0] == "!":
        AsciiArt(stext)
    else:
        print_(stext)
        try:
            server_socket.send(stext)
        except:
            print_("Problem while sending text...")


def print_(rdata):
    global line11
    if len(rdata) > 0:
        rdata= rdata + '\n'
    line11 +=1.0
    text1.config(state=NORMAL)
    text1.insert(line11, rdata)
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
    GUI_Running_thread = threading.Thread(target=Main_GUI)
    GUI_Running_thread.start()
    time.sleep(5)
    

    Server_Running_thread =threading.Thread(target=Server)
    Server_Running_thread.start()

    
def Server():
    global server_socket
    host = "10.1.237.2"
    port = 8421
     
    server_socket = socket.socket()
    server_socket.settimeout(2)
    server_socket.connect((host, port))
    print_("Connected to remote host. You can now send messages")
    
     
    while True:
        socket_list = [sys.stdin, server_socket]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for current_socket in read_sockets:
            if current_socket == server_socket:
                rdata = current_socket.recv(4096)
                if not rdata:
                    print_("Disconnected from chat server")
                    server_socket.close()
                    sys.exit()
                else:
                    print_(rdata)
                    
            else:
                server_socket.send(stext)
     
line11=1
if __name__ == "__main__":
    main()
  
