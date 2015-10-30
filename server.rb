require 'socket'
require 'thread'

PORT = 8421
socket = TCPServer.new('127.0.0.1', PORT)


def handle_connection(client)
   puts "Client #{client} has connected"

end

puts "[#{Time.now}]: Listening on #{PORT}."

while client = socket.accept
	Thread.new { handle_connection(client) }
		client.puts "---Connection Established---"
		client.puts "-----------Login-----------"
		client.puts "Enter command.\n1. Alias\n2. Anonymous Alias\n3. Create Account"
		command = client.gets.chomp
		if command = "1"
			client.puts "Please enter an Alias"
			Alias = client.gets.chomp
		elseif command = "2"
			Alias = "anon"
		elseif command = "3"
			client.puts "Feature not available yet"
		else client.puts "Command not valid please enter another command"
		end
end
