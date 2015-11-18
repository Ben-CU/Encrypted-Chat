import select
import socket
import sys

ConnectionList = [] # List that holds all of the sockets that connect
ServerSocket = socket.socket() # The socket that the server runs on

def SendMessage(SendingSocket, Message):
	"""
	Function that sends a message to every socket apart from the server and the sender
	"""
	for CurrentSocket in ConnectionList:
		if (CurrentSocket != ServerSocket) and (CurrentSocket != SendingSocket):
                        CurrentSocket.send(Message)

def GetHostIP():
        """
        Gets the IP for the server and if the server is to be running on a LAN or not
        """
        sys.stdout.write("Is this a LAN server ( y/n ): ")
        UserInput = sys.stdin.readline()
        if (UserInput[0] == "y") or (UserInput[0] == "Y"):
                import os
                LocalIP = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
                return LocalIP.read()     
        elif (UserInput[0] == "n") or (UserInput[0] == "N"):
                import urllib
                IP = urllib.urlopen('http://simplesniff.com/ip').read()
                IP = str(IP[0:-1])
                return IP
        else:
                print("That is not a valid choice, please try again")
                GetHostIP()

def Main():
	"""
	The main function that creates the server and runs it everything runs from here
	"""
	HostIP = GetHostIP()
	Port = 8421
	
	# Binds the IP and port to that socket then sets to listen for incoming data/connections
	ServerSocket.bind((HostIP,Port))
	ServerSocket.listen(20)
	ConnectionList.append(ServerSocket)

	print("The server has been started on")
	sys.stdout.write("Host: " + HostIP)
	print("Port: " + str(Port))
	
	# The main part of the server that loops round forever or till the server shuts down
	while True:
		# The list of sockets which are ready to be read through select
		ReadSockets, WriteSockets, ErrorSockets = select.select(ConnectionList,[],[])

		for CurrentSocket in ReadSockets:
			if CurrentSocket == ServerSocket:
				# A new client connects to the server
				NewSocket, ClientAddress = ServerSocket.accept()
				ConnectionList.append(NewSocket)
				print("Client from " + str(ClientAddress) + " has connected")
			else:
				# A client has sent a message
				NewMessage = CurrentSocket.recv(4096)
				if NewMessage:
                                        sys.stdout.write(str(CurrentSocket) + " " + NewMessage)
					SendMessage(CurrentSocket, NewMessage)
	 
	ServerSocket.close()

if __name__ == "__main__":
	Main()
