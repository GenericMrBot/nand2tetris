keywords = ["class", "constructor", "function", "method", "field",
            "static", "var", "int", "char", "boolean", "void",
            "true", "false", "null", "this", "let", "do", "if",
            "else", "while", "return"]

symbols = ["{", "}", "(", ")", "[",
           "]", ".", ",", ";", "+",
           "-", "*", "/", "&", "|",
           "<", ">", "=", "~"]


def newParse(file):
    with open(file, "r") as file:
        contents = file.readlines()
    # removes single line comments
    contents = [lines.split("//")[0] for lines in contents]

    # removes blank lines
    contents = [lines for lines in contents if lines !=
                "\n" and len(lines) > 0 and lines != "\t\n"]

    # removes multi-line comments
    tempcontents = []
    switch = True
    for line in contents:
        if "/**" in line:
            switch = False
        if switch:
            tempcontents.append(line)
        if "*/" in line[-3:]:
            switch = True
    contents = tempcontents

    # join into single string
    thing = ""
    contents = thing.join(contents)

    # get rid of new lines and tabs and big whitespace
    contents = contents.replace("\n", "")
    contents = contents.replace("\t", "")
    contents = contents.replace("    ", "")

    # parse + create lexList
    wordList = []
    lexList = []
    isStr = False
    isInt = False
    nextWord = ""

    for i, e in enumerate(contents):
        # stringConstant
        if e == '"':
            # print("1")
            if isStr == False:
                nextWord = e
                isStr = True
                continue
            if isStr == True:
                nextWord += e
                nextWord = nextWord.removeprefix('"').removesuffix('"')
                wordList.append(nextWord)
                lexList.append("stringConstant")
                nextWord = ""
                isStr = False
                continue
        if isStr:
            nextWord += e
            continue

        # integerConstant
        if e in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            # print("2")
            if isInt == False:
                nextWord = e
                # print(nextWord)
                isInt = True
            elif isInt == True:
                nextWord += e

            if not(contents[i+1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
                # print(f"3: {nextWord}")
                wordList.append(nextWord)
                lexList.append("integerConstant")
                nextWord = ""
                isInt = False
                continue
            else:
                continue

        if i == len(contents):
            endWord = (i == len(contents))             # end of file
        elif i < len(contents)-1:
            endWord = contents[i+1] == " "           # space
            # ended by symbol
            endWord = endWord or contents[i+1] in symbols
            if i == len(contents)-1:        # ended by new at the end of the file
                endWord = endWord or contents[i+1:] == "\n"
            elif i < len(contents)-1:
                # ended by new line
                endWord = endWord or contents[i+1:i+3] == "\n"

        # keywordConstant
        nextWord += e
        nextWord = nextWord.removeprefix(" ")
        if nextWord in keywords and endWord:
            wordList.append(nextWord)
            lexList.append("keyword")
            nextWord = ""
            continue

        if e in symbols:
            wordList.append(e)
            lexList.append("symbol")
            nextWord = ""
            continue

        # identifier
        if len(nextWord) > 0:
            if nextWord[0] != "_" and endWord:
                wordList.append(nextWord)
                lexList.append("identifier")
                nextWord = ""
                continue

            # symbol

    tempWords = wordList

    # last min parsing
    for i, word in enumerate(tempWords):
        if word == "":
            del wordList[i]
            del lexList[i]
    return wordList, lexList


#######################################
# everything below this was a bad attempt
######################################


def initialClean(file):
    '''
    args: (file) file path
    returns: (list of lists) prog = [line, line], line = [word, word]
        - removed comment + blank lines
        - split at spaces
    '''

    with open(file, "r") as file:
        contents = file.readlines()
    # removes multi-line comments
    tempcontents = []
    switch = True
    for line in contents:
        if line[0:3] == "/**":
            switch = False
        if switch:
            tempcontents.append(line)
        if "*/" in line[-3:]:
            switch = True
    contents = tempcontents

    # removes single line comments
    contents = [lines.split("//")[0] for lines in contents]
    # removes new lines
    contents = [lines.strip() for lines in contents]
    # removes blank lines
    contents = [lines for lines in contents if len(
        lines) > 0]
    # gets rid of white space
    contents = [lines.split() for lines in contents]

    # try to get comments in the middle of the line
    # and /*/
    return contents


def splitSymbols(contents):
    '''
    args: (contents) list of words not seperating "symbols"
    returns: (contents) list of words seperating "symbols
    '''
    combine = ""
    for line in contents:
        for word in line:
            combine += word + " "
    tempcomb = ""
    for l in range(len(combine)):
        if combine[l] in symbols:
            tempcomb += " " + combine[l] + " "
        else:
            tempcomb += combine[l]
    combine = tempcomb
    l = combine.split(" ")

    contents = [word for word in l if len(word) > 0]
    # print(contents)

    # address strings
    return contents


def addStrings(contents):
    print(contents)
    for i, word in enumerate(contents):
        if word[0] == '"':
            print(word)
            leave = False
            while leave == False:
                print(contents[i+1] == '"')
                if contents[i][-1] == '"':
                    leave = True
                elif contents[i+1][-1] == '"':
                    contents[i] += " " + contents[i+1]
                    print(word)
                    del contents[i+1]
                    leave = True
                else:
                    word += " " + contents[i+1]
                    del contents[i+1]

            # print(word)
    print(contents)
    return contents


def createlexicallist(contents):
    '''
    args: (contents) list of lexical elements yet to be categorized
    return: (list) of lexical identifiers corresponding to that of the
        input list
    '''
    lexlist = []
    for i, e in enumerate(contents):
        print(i, e)
        if e in keywords:
            lexlist.append("keywordConstant")
            continue
        elif e in symbols:
            lexlist.append("symbol")
        # figure out if string and first aren't _ or whatever
        elif e[0] == '"' and e[-1] == '"':
            lexlist.append("stringConstant")
        elif all(e[i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] for i in range(len(e))):
            lexlist.append("integerConstant")
        elif e[0] != "_":
            lexlist.append("identifier")
        else:
            print(f"lexical error {e} is not something that I can parse")
            raise
    return lexlist
