require "socket"
require "gibberish"

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
    cipher = Gibberish::AES.new('Password')
    @response = Thread.new do
      loop {
        msg = @server.gets.chomp
        plainmsg = cipher.decrypt(msg)
        puts "#{plainmsg}"
      }
    end
  end

  def send
    cipher = Gibberish::AES.new('Password')
    puts "Enter an Alias:"
    @request = Thread.new do
      loop {
        plainmsg = $stdin.gets.chomp
        msg = cipher.encrypt(plainmsg)
        @server.puts( msg )
      }
    end
  end
end

server = TCPSocket.open( "10.1.200.19", 8421 )
Client.new( server )
