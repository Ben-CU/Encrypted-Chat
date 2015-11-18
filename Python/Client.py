import select
import socket
import string
import sys
 
def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()
 
def Main():
    Host = "192.168.133.129"
    Port = 8421
     
    ServerSocket = socket.socket()
    ServerSocket.settimeout(2)
    ServerSocket.connect((Host, Port))
     
    print 'Connected to remote host. You can now send messages'
    prompt()
     
    while True:
        socket_list = [sys.stdin, ServerSocket]
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            if sock == ServerSocket:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    prompt()
            else :
                msg = sys.stdin.readline()
                ServerSocket.send(msg)
                prompt()

if __name__ == "__main__":
    Main()
