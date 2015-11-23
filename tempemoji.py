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
        print("Valid Picture Commands are:")
        for file in names:
            print(file)
    elif inputstring in names2:
        file = inputstring.replace("!", "")
        filepath = "AsciiArt/" + file + ".txt"
        output = open(filepath, 'r').read()
        print (output)
    else:
        print("This is not a valid command! Try '!help'")
