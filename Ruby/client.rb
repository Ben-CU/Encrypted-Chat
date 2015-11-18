require "socket"

class Client
  def initialize( server )
    @server = server
    @request = nil
    @response = nil
    listen
    send
    @request.join
    @response.join
  end

  def listen
    @response = Thread.new do
      loop {
        msg = @server.gets.chomp
        puts "#{msg}"
      }
    end
  end
  
  def AsciiArt( inputstring )
    if inputstring == "help"
	  puts "Valid Picture Commands Are:"
	  files = Dir["AsciiArt/**/*.txt"]
	  files.each do |file_name|
        if !File.directory? file_name
          commandname = "!" + file_name.slice(9..-5)
		  puts commandname
	    end
	  end
	else
      begin
	    filepath = "AsciiArt/" + inputstring + ".txt"
	    output = IO.readlines(filepath)
	    return output
	  rescue
	    puts "That ascii picture isnt present try !help for valid pictures commands"
	  end
	end
  end

  def send
    puts "Enter an Alias:"
    @request = Thread.new do
      loop {
        msg = $stdin.gets.chomp
		if msg.split('')[0] == '!'
			msgtoserver = AsciiArt( msg.slice(1..-1) )
			@server.puts( msgtoserver )
		else
			@server.puts( msg )
		end
      }
    end
  end
end

server = TCPSocket.open( "10.89.202.179", 8421 )
Client.new( server )
