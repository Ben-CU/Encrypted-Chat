def emoji (m)
  def read_file(file_name)
    file = File.open(file_name, "r")
    data = file.read
    file.close
    return data
  end
  if m.include? "/bigmona"
    mona = read_file("asciiart/mona.txt")
  end

  if m.include? "/dickbutt"
    dickbutt = read_file("asciiart/dickbutt.txt")
  end

  if m.include? "/happy"
    happy = read_file("asciiart/happy.txt")
  end




  m.sub! '/bigmona', mona
  m.sub! '/dickbutt', dickbutt
  m.sub! '/happy', ':D'
  m.sub! '/etower', "h"
  return m
end





 puts emoji("/bigmona /dickbutt")






def read_file(file_name)
  file = File.open(file_name, "r")
  data = file.read
  file.close
  return data
end
