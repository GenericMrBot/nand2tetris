import os
import sys
import Tokenizer
import Parser

jfolder = sys.argv[1]


def analyzeJackFile(file, classNames):
    """
    args: (file) jack file path
    returns: xml file
    """

    tokens, lexLabels = Tokenizer.newParse(file)

    # token formatting
    for i, e in enumerate(lexLabels):
        if tokens[i] == "<":
            lexLabels[i] = f"<{e}> &lt; </{e}>"
        elif tokens[i] == "&":
            lexLabels[i] = f"<{e}> &amp; </{e}>"
        elif tokens[i] == ">":
            lexLabels[i] = f"<{e}> &gt; </{e}>"
        else:
            lexLabels[i] = f"<{e}> {tokens[i]} </{e}>"

    xmlfile = Parser.GetXML(tokens, lexLabels, file, classNames)
    xmlfile.getXML()
    xmlfile.writeXML()
    return


def que(jfolder):
    '''
    args: jfolder (folder or jack file) 
    outputs: (list) of paths to all jack files in the folder
    '''
    qfiles = []
    filenames = []
    print(f"queing files...")

    if jfolder[-5:] == ".jack":
        print(f'File: {jfolder}, cued for compiling')
        return [jfolder]

    for thing in os.listdir(jfolder):
        if thing.endswith(".jack"):
            print(f'File: {os.path.join(jfolder, thing)}, cued for compiling')
            qfiles.append(os.path.join(jfolder, thing))
            filenames.append(thing.removesuffix('.jack'))
    return qfiles


def write_to_file(text, filename):
    with open(filename, "w") as file:
        file.write(text)


def main(jfolder):
    '''
    args: jfolder (folder or jack file)
    returns: xml file
    '''
    classNames = []
    qfiles = que(jfolder)
    for file in qfiles:
        classNames.append(file.split("/")[-1].split(".")[0])
    for file in qfiles:
        analyzeJackFile(file, classNames)


main(jfolder)
