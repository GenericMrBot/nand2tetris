'''
so statements takes the list of remaining tokens and feeds it back into statemnt
then that feeds it into if while and whatever
then each of those feeds it into each of the key word functions
and it should recursively go through it
key word functions should return both the parse tree parts and the remaining thing
so three things really [parse tree parts, correspondign identifiers, remaining key words]
never mind this is all shit

ok so for the xml I think I've gotta just make a string. I'll store the beginning and
the end seperately and join them at the end/. That way I can just add to the middle and
make it simple like that.
in the end I have to
que files
loop through files
end up with getting an xml file for each file
along the way I have to do error checking
'''
import time


class GetXML:
    def __init__(self, tokens, lexLabels, file, classNames):
        self.tokens = tokens
        self.Rtokens = tokens       # stands for remaining tokens
        self.lexLabels = lexLabels
        self.RlexLabels = lexLabels  # remaining labels to be added to xml
        self.varNames = []
        self.subroutineNames = []
        self.classNames = classNames
        self.file = file
        self.filename = self.file.split("/")[-1].split(".")[0]
        self.xml = ""
        self.op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        self.unaryOp = ['-', '~']
        self.KeywordConstant = ['true', 'false', 'null', 'this']
        self.tabLevel = 0

    def writeXML(self):
        filename = self.file
        filename = filename.removesuffix(".jack") + "ME"
        with open(f"{filename}.xml", "w") as thing:
            thing.write(self.xml)              # write to file
        print(f"{self.filename}ME.xml contains the assembly translation")

    def getXML(self):
        self.JackClass()

    def xmlAdd(self):
        # helper func to make it easy to add to the current xml thing
        # and increment the next word to add

        for i in range(self.tabLevel):
            self.xml += "  "
        self.xml += self.RlexLabels[0]
        self.xml += "\n"
        self.Rtokens = self.Rtokens[1:]
        self.RlexLabels = self.RlexLabels[1:]

    def nextIsStatement(self):
        # self explanitory
        statementStarts = ["let", "if", "while", "do", "return"]
        if self.Rtokens[0] in statementStarts:
            return True
        else:
            return False

    def beginTag(self, tag):
        for i in range(self.tabLevel):
            self.xml += "  "
        self.xml += tag + "\n"
        self.tabLevel += 1

    def endTag(self, tag):
        self.tabLevel -= 1
        for i in range(self.tabLevel):
            self.xml += "  "
        self.xml += tag + "\n"

    def nextParenthesis(self, char):
        # helper func specifically for parenthesis error checking
        # mainly for keeping code DRY
        if self.Rtokens[0] == char:
            self.xmlAdd()
        else:
            print(f"missing an open parenthesis: {char}")
            raise

    def wrapBody(self, char1, char2, func):
        # another common structure we see
        # doing this to keep things DRY and more simple
        self.nextParenthesis(char1)
        func()
        self.nextParenthesis(char2)

    def isVarName(self):
        if self.Rtokens[0] in self.varNames:
            return True
        return False

    def isClassName(self):
        if self.Rtokens[0] in self.classNames:
            return True
        return False

    def isSubroutineName(self):
        # print("7")
        if self.Rtokens[0] in self.subroutineNames:
            return True
        return False

    #######################
    ## Program Structure ##
    #######################

    def JackClass(self):
        # initial checks of class name matching filename
        if self.file.split("/")[-1].split(".")[0] != self.tokens[1]:
            print("class name does not match file name")
            raise
        if self.tokens[0] != "class":
            print('umm start this with a "class" pls')
            raise

        self.beginTag("<class>")

        ## strucutre ##
        # 'class' className '{' classVarDec* subroutineDec* '}'

        if self.tokens[0] == "class":
            self.xmlAdd()
        else:
            print(f"{self.tokens[0]} is not 'class'")

        self.xmlAdd()  # class name
        self.xmlAdd()  # {

        # classVarDec*
        self.classVarDec()

        # subroutineDec*
        self.subroutineDec()

        self.xmlAdd()  # {

        self.endTag("</class>")

    def classVarDec(self):
        ## strucutre ##
        # ('static' | 'field') type varName (',' varName)* ';'
        if self.Rtokens[0] == ",":
            self.xmlAdd()      # ,
            self.varName()      # varName
            self.classVarDec()  # recursion
            return
        if self.Rtokens[0] == "static" or self.Rtokens[0] == "field":
            self.beginTag("<classVarDec>")
            self.xmlAdd()      # ('static' | 'field')
            self.type()         # type
            self.varName()      # varName
            self.classVarDec()  # (',' varName)* handled in base case
            self.xmlAdd()      # ';'
            self.endTag("</classVarDec>")
            self.classVarDec()
            return

    def type(self):  # done I think
        ## strucutre ##
        # 'int' | 'char' | 'boolean' | className
        thing = ['int', "char", 'boolean', 'String']
        if self.Rtokens[0] in thing:
            self.xmlAdd()  # add type
        else:
            self.xmlAdd()   # add classname

    def subroutineDec(self):
        self.beginTag("<subroutineDec>")

        ## strucutre ##
        # ('constructor' | 'function' | 'method')
        # ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        things = ['constructor', 'function', 'method']
        if self.Rtokens[0] in things:
            self.xmlAdd()
        else:
            print(f"invalid subroutine declaration: {self.Rtokens[0]}")
            raise

        if self.Rtokens[0] == "void":
            self.xmlAdd()   # add the void keyword
        else:
            self.type()
        if "identifier" in self.RlexLabels[0]:
            self.xmlAdd()
        else:
            print(f"{self.Rtokens[0]} is not an identifier")
            raise

        self.wrapBody("(", ")", self.paramList)  # '(' parameterList ')'

        self.subroutineBody()

        self.endTag("</subroutineDec>")

        if self.Rtokens[0] in ['function', 'method']:
            self.subroutineDec()

    def paramList(self):

        ## strucutre ##
        # ((type varName) (',' type varName)*)?
        self.beginTag("<parameterList>")

        if self.Rtokens[0] == ")":
            self.endTag("</parameterList>")
            return

        self.type()

        self.varName()

        while (self.Rtokens[0] == ","):
            self.xmlAdd()
            self.type()
            self.varName()

        self.endTag("</parameterList>")

    def subroutineBody(self):
        self.beginTag("<subroutineBody>")

        ## strucutre ##
        # '{' varDec* statements '}'

        # opening {
        self.nextParenthesis("{")
        # if self.Rtokens[0] == "{":
        #     self.xmlAdd()
        # else:
        #     print("missing {")
        #     raise
        self.varDecs()      # varDec*

        self.beginTag("<statements>")
        self.Statements()   # statements

        # end }
        self.nextParenthesis("}")
        # if self.Rtokens[0] == "}":
        #     self.xmlAdd()
        # else:
        #     print("missing }")
        #     raise

        self.endTag("</subroutineBody>")

    def varDecs(self):  # done I think

        if self.Rtokens[0] == "var":
            self.varDec()
            self.varDecs()  # for recursion purposes
        elif self.nextIsStatement():
            return
        else:
            print(
                f"error neither beginning a statement or declaring a var: {self.Rtokens[0]}")
            raise

    def varDec(self):   # done I think
        ## strucutre ##
        # 'var' type varName (',' varName)* ';'
        if self.Rtokens[0] == ",":
            self.xmlAdd()  # ,
            self.varName()  # varName
            self.varDec()   # for recursion purposes
        elif self.Rtokens[0] == "var":
            self.beginTag("<varDec>")
            self.xmlAdd()  # var
            self.type()     # type
            self.varName()  # varName
            self.varDec()
            self.endTag("</varDec>")
            return
        elif self.Rtokens[0] == ";":
            self.xmlAdd()  # ;
        else:
            print(f"something ain't adding up here")
            time.sleep(5)
            print(f"here's the error: invalid varriable declaration")
            raise

    def varName(self):
        self.varNames.append(self.Rtokens[0])
        self.xmlAdd()

    def subroutineName(self):
        self.subroutineNames.append(self.Rtokens[0])
        self.xmlAdd()

    #########################
    ## Statement functions ##
    #########################

    def Statements(self):
        '''
        args:
        returns:
        recursively goes through tokens to arive at the bottom layer of the parse tree
        '''
        ## strucutre ##
        # statement*

        if self.nextIsStatement():
            self.Statement()
            self.Statements()
        elif self.Rtokens[0] == "}":  # ie it is the end of the body of a thing
            self.endTag("</statements>")
        else:
            print(
                f"umm something went wrong when going between statements or out of a statement block")
            time.sleep(2)
            raise

    def Statement(self):
        '''
        args:
        returns:
        '''
        ## strucutre ##
        # letStatement | ifStatement | whileStatement | doStatement | returnStatement

        if self.Rtokens[0] == "if":
            self.ifStatement()
        elif self.Rtokens[0] == "while":
            self.whileStatement()
        elif self.Rtokens[0] == "let":
            self.letStatement()
        elif self.Rtokens[0] == "do":
            self.doStatement()
        elif self.Rtokens[0] == "return":
            self.returnStatement()
        else:   # I don't think it can ever get here
            print(
                f'{self.Rtokens[0]} in line __ is not a recognized statement type')

    def letStatement(self):
        ## strucutre ##
        # 'let' varName ('[' expression ']')? '=' expression ';'
        self.beginTag("<letStatement>")

        self.xmlAdd()      # let
        self.varName()      # varName

        if self.Rtokens[0] == "[":
            self.wrapBody("[", "]", self.expression)
        if self.Rtokens[0] == "=":
            self.wrapBody("=", ";", self.expression)
        else:
            print("things ain't adding up here")
            time.sleep(3)
            print("ahh I see, somethings up with the = sign in this let statement")
            raise

        self.endTag("</letStatement>")

    def ifStatement(self):
        self.beginTag("<ifStatement>")

        ## strucutre ##
        # 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?

        self.xmlAdd()  # if

        self.wrapBody("(", ")", self.expression)

        self.nextParenthesis("{")
        self.beginTag("<statements>")
        self.Statements()
        self.nextParenthesis("}")

        if self.Rtokens[0] == "else":
            self.xmlAdd()
            self.nextParenthesis("{")
            self.beginTag("<statements>")
            self.Statements()
            self.nextParenthesis("}")
        elif self.nextIsStatement or self.Rtokens[0] == "}":
            self.endTag("</ifStatement>")
            return
        else:
            print("invalid if statement")
            raise

        self.endTag("</ifStatement>")

    def whileStatement(self):
        ## strucutre ##
        # 'while' '(' expression ')' '{' statements '}'
        self.beginTag("<whileStatement>")

        self.xmlAdd()      # let

        self.wrapBody("(", ")", self.expression)

        self.nextParenthesis("{")
        self.beginTag("<statements>")
        self.Statements()           # statements block
        self.nextParenthesis("}")

        self.endTag("</whileStatement>")

    def doStatement(self):
        ## strucutre ##
        # 'do' subroutineCall ';'
        self.beginTag("<doStatement>")

        self.xmlAdd()      # do

        self.subroutineCall()

        if self.Rtokens[0] == ";":
            self.xmlAdd()
        else:
            print("something went wrong in the do statement")
        self.endTag("</doStatement>")

    def returnStatement(self):
        ## strucutre ##
        # 'return' expression? ';'
        self.beginTag("<returnStatement>")

        self.xmlAdd()      # return

        if self.Rtokens[0] == ";":
            self.xmlAdd()
        else:
            self.expression()   # this will handle exceptions
            if self.Rtokens[0] == ";":
                self.xmlAdd()  # ;

        self.endTag("</returnStatement>")

    ##########################
    ## Identifier Funcitons ##
    ##########################

    def expression(self):
        ## strucutre ##
        # term (op term)*

        self.beginTag("<expression>")
        self.term()

        while self.Rtokens[0] in self.op:
            self.xmlAdd()
            self.term()

        self.endTag("</expression>")

    def term(self):
        ## strucutre ##
        # integerConstant | stringConstant | keywordConstant | varName |
        # varName '[' expression ']' | subroutineCall | '(' expression ')' |
        # unaryOp term

        self.beginTag("<term>")
        if self.Rtokens[0] in self.unaryOp:
            self.xmlAdd()  # this handles the unary op stuff
            self.term()

        elif self.Rtokens[0] in self.KeywordConstant:
            self.xmlAdd()

        elif "Constant" in self.RlexLabels[0]:
            self.xmlAdd()

        elif self.Rtokens[1] == "[":
            # print("3")
            self.xmlAdd()
            self.nextParenthesis("[")
            self.expression()
            if self.Rtokens[0] == "]":
                self.xmlAdd()
            else:
                print("umm error in term prolly missing end bracket ]")
                raise

        elif self.Rtokens[0] == "(":
            self.wrapBody("(", ")", self.expression)

            # self.xmlAdd()
            # self.expression()
            # if self.Rtokens[0] == ")":
            #     self.xmlAdd()
            # else:
            #     print("prolly missing end parenthesis")
            #     raise

        elif self.isVarName():
            self.xmlAdd()
            if self.Rtokens[0] == '[':  # is this 1 or 0?
                self.wrapBody("[", "]", self.expression)

        elif self.Rtokens[1] in [".", "("]:
            self.subroutineCall()
        else:
            print("invalid term expression")
            raise

        self.endTag("</term>")

    def subroutineCall(self):
        ## strucutre ##
        # subroutineName '(' expressionList ')' | (className |
        # varName) '.' subroutineName '(' expressionList ')'

        if self.Rtokens[1] == ".":

            self.xmlAdd()  # classname or varname
            self.xmlAdd()  # .

        self.xmlAdd()  # subroutinename
        if (self.Rtokens[0] != "("):
            print("what the hell")
            raise

        self.wrapBody("(", ")", self.expressionList)
        # self.xmlAdd()  # (
        # self.expressionList()
        # self.xmlAdd()   # )

    def expressionList(self):
        ## strucutre ##
        # (expression (',' expression)* )?
        self.beginTag("<expressionList>")

        if self.Rtokens[0] == ")":
            self.endTag("</expressionList>")
            return

        self.expression()

        while(self.Rtokens[0] == ","):
            self.xmlAdd()
            self.expression()

        self.endTag("</expressionList>")
