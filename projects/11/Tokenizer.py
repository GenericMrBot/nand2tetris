from hashlib import new


keywords = ["class", "constructor", "function", "method", "field",
            "static", "var", "int", "char", "boolean", "void",
            "true", "false", "null", "this", "let", "do", "if",
            "else", "while", "return"]

symbols = ["{", "}", "(", ")", "[",
           "]", ".", ",", ";", "+",
           "-", "*", "/", "&", "|",
           "<", ">", "=", "~"]


def initialClean(file):
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
    contents = contents.replace("\n", "")
    contents = contents.replace("\t", "")
    contents = contents.replace("    ", "")

    return contents


def newParse(file):

    contents = initialClean(file)

    # parse + create lexList
    wordList = []
    lexList = []
    isStr = False
    isInt = False
    nextWord = ""
    for i, e in enumerate(contents):
        # stringConstant
        if e == '"':
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
            endWord = i == len(contents)                        # end of file
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

    tempWords = wordList
    for i, word in enumerate(tempWords):
        if word == "":
            del wordList[i]
            del lexList[i]

    return wordList, lexList


def Tokenizer(file):

    tokens, lexLabels = newParse(file)

    for i, e in enumerate(lexLabels):
        if tokens[i] == "<":
            lexLabels[i] = f"<{e}> &lt; </{e}>"
        elif tokens[i] == "&":
            lexLabels[i] = f"<{e}> &amp; </{e}>"
        elif tokens[i] == ">":
            lexLabels[i] = f"<{e}> &gt; </{e}>"
        elif tokens[i] == '"':
            lexLabels[i] = f"<{e}> &quot; </{e}>"
        else:
            lexLabels[i] = f"<{e}> {tokens[i]} </{e}>"
    return tokens, lexLabels
