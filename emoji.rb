def emoji (m)
  f = IO.readlines("econtent.txt")
  m.sub! '/bigmona', f[0,70].to_s
  m.sub! '/dickbutt', f[76,149].to_s
  return m
end






# puts emoji("/dickbutt")









#ignore
def read_file(file_name)
  file = File.open(file_name, "r")
  data = file.read
  file.close
  return data
end
