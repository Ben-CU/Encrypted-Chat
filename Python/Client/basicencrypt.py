import datetime
import sys

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
            "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ",", ".", "-", "(", ")", "!", "|", "?", "0", "1", "2",
            "3", "4", "5", "6", "7", "8", "9", ":"]

def encrypt(message_to_encrypt):
    length = len(alphabet)
    message_to_encrypt = message_to_encrypt.replace(' ', '|')
    key = str(datetime.date.today())
    messagelength = len(message_to_encrypt)
    encrypted_message = []
    count = 0
    keylist = []
    messagelist = []
    output = []
    i = 0
    for char in key:
        keylist.append(alphabet.index(char))
    for char in message_to_encrypt:
        messagelist.append(alphabet.index(char))
    while count < messagelength:
        encrypted_message.append((messagelist[i] + keylist[i]) % length)
        count += 1
        i += 1
    for N in encrypted_message:
        output.append(alphabet[N])
    return ''.join(output)

def decrypt(message_to_decrypt):
    length = len(alphabet)
    message_to_decrypt = message_to_decrypt.replace(' ', '|')
    key = str(datetime.date.today())
    keylength = len(key)
    messagelength = len(message_to_decrypt)
    overlap = messagelength % keylength
    leftover = key[:overlap]
    random = messagelength / keylength
    key = (int(random) * key) + leftover
    decrypted_message = []
    count = 0
    keylist = []
    messagelist = []
    output = []
    i = 0
    for char in key:
        keylist.append(alphabet.index(char))
    for char in message_to_decrypt:
        messagelist.append(alphabet.index(char))
    while count < messagelength:
            decrypted_message.append((messagelist[i] - keylist[i]) % length)
            count += 1
            i += 1
    for N in decrypted_message:
        output.append(alphabet[N])
    count = 0
    for char in output:
        if char == '|':
            output[count] = ' '
            count += 1
        else:
            count += 1
    return ''.join(output)


if __name__ == "__main__":
    print("This module is not meant to be run on its own")
    sys.exit()
