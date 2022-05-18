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
from SymbolTable import *


class JackCompiler:
    def __init__(self, tokens, lexLabels, file, classNames):
        self.tokens = tokens
        self.Rtokens = tokens       # stands for remaining tokens
        self.lexLabels = lexLabels
        self.RlexLabels = lexLabels  # remaining labels to be added to xml
        self.varNames = []
        self.subroutineNames = []
        # TODO: figure out all class types
        self.classNames = ["Array", "Math", "Keyboard",
                           "String", "Sys", "Output", "Screen", "Memory"]
        self.classNames = self.classNames + classNames
        self.file = file
        self.filename = self.file.split("/")[-1].split(".")[0]
        self.vm = ""
        self.op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        self.unaryOp = ['-', '~']
        self.KeywordConstant = ['true', 'false', 'null', 'this']
        self.tabLevel = 0
        self.statics = []
        self.fields = []
        self.arguements = []
        self.locals = []

    def writeVM(self):
        filename = self.file
        filename = filename.removesuffix(".jack")
        with open(f"{filename}.vm", "w") as thing:
            thing.write(self.vm)              # write to file
        print(f"{self.filename}.vm contains the assembly translation")

    def getXML(self):
        self.JackClass()

    def writeFunc(self):
        self.vm += f"function {self.filename}.{self.Rtokens[0]}"
        # TODO: change 0 when symbol table works

    def nextToken(self):
        self.Rtokens = self.Rtokens[1:]
        self.RlexLabels = self.RlexLabels[1:]

    def eatToken(self, string):
        # helper func
        if self.Rtokens[0] == string:
            self.nextToken()
            return self.Rtokens[0]
        else:
            print(f"Expected {string} got {self.Rtokens[0]}")
            raise

    def nextIsStatement(self):
        # self explanitory
        statementStarts = ["let", "if", "while", "do", "return"]
        if self.Rtokens[0] in statementStarts:
            return True
        else:
            return False

    def wrapBody(self, char1, char2, func):
        # another common structure we see
        # doing this to keep things DRY and more simple
        self.eatToken(char1)
        out = func()
        self.eatToken(char2)
        return out

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

    ##########################
    ## Symbol Table Helpers ##
    ##########################

    def findLocal(self, varname):
        for i, e in enumerate(self.locals):
            if e[0] == varname:
                return f"local {i}"

    #######################
    ## Program Structure ##
    #######################

    def Compile(self):
        # initial checks of class name matching filename
        if self.file.split("/")[-1].split(".")[0] != self.tokens[1]:
            print("class name does not match file name")
            raise

        ## strucutre ##
        # 'class' className '{' classVarDec* subroutineDec* '}'

        if self.tokens[0] == "class":
            self.nextToken()
        else:
            print(f"{self.tokens[0]} is not 'class'")
            raise

        self.nextToken()  # class name
        self.nextToken()  # {

        # classVarDec*
        self.classVarDec()

        print("1")
        # subroutineDec*
        self.subroutineDec()

        self.nextToken()  # {

    def classVarDec(self):
        ## strucutre ##
        # ('static' | 'field') type varName (',' varName)* ';'
        if self.Rtokens[0] == ",":
            self.nextToken()      # ,
            self.varName()      # varName
            self.classVarDec()  # recursion
            return
        if self.Rtokens[0] == "static" or self.Rtokens[0] == "field":
            self.nextToken()      # ('static' | 'field')
            self.type()         # type
            self.varName()      # varName
            self.classVarDec()  # (',' varName)* handled in base case
            self.nextToken()      # ';'
            self.classVarDec()
            return

    def type(self):  # done I think
        ## strucutre ##
        # 'int' | 'char' | 'boolean' | className
        thing = ['int', "char", 'boolean', 'String']
        if self.Rtokens[0] in thing:
            thing = self.Rtokens[0]
            self.nextToken()  # add type
            return thing
        elif self.Rtokens[0] in self.classNames:
            thing = self.Rtokens[0]
            self.nextToken()  # add classname
            return thing
        else:
            print(f"not an accepted type {self.Rtokens[0]}")
            raise

    def subroutineDec(self):
        ## strucutre ##
        # ('constructor' | 'function' | 'method')
        # ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        yesMethod = 0
        things = ['constructor', 'function', 'method']
        if self.Rtokens[0] in things:
            if self.Rtokens[0] == "method":
                yesMethod = 1
            self.nextToken()
        else:
            print(f"invalid subroutine declaration: {self.Rtokens[0]}")
            raise

        if self.Rtokens[0] == "void":
            self.nextToken()   # add the void keyword
            returnme = "push constant 0\n"
        else:
            self.type()
            returnme = ""  # just return the top of the stack

        if "identifier" in self.RlexLabels[0]:
            self.writeFunc()    # subroutine name TODO
            self.nextToken()
        else:
            print(f"{self.Rtokens[0]} is not an identifier")
            raise

        # '(' parameterList ')'
        num_params = self.wrapBody("(", ")", self.paramList)

        self.subroutineBody(yesMethod)

        # idk if this is right
        self.vm += f"{returnme}"
        self.vm += f"return\n"

        if self.Rtokens[0] in ['function', 'method']:
            self.subroutineDec()

    def paramList(self):
        ## strucutre ##
        # ((type varName) (',' type varName)*)?
        count = 0
        if self.Rtokens[0] == ")":
            return count

        self.type()
        self.varName()
        count += 1

        while (self.Rtokens[0] == ","):
            self.nextToken()
            self.type()
            self.varName()
            count += 1

        return count

    def subroutineBody(self, isMethod):
        ## strucutre ##
        # '{' varDec* statements '}'

        # opening {
        self.eatToken("{")

        count = isMethod    # if method then 1 else 0
        count = self.varDecs()      # varDec*
        print(count)
        self.vm += f" {count}\n"

        # number at the end of function declaration

        self.Statements()   # statements

        # end }
        self.eatToken("}")

    def varDecs(self):  # done I think
        count = 0

        if self.Rtokens[0] == "var":
            count += self.varDec()
            count += self.varDecs()  # for recursion purposes
            return count
        elif self.nextIsStatement():
            return count
        else:
            print(
                f"error neither beginning a statement or declaring a var: {self.Rtokens[0]}")
            raise

    def varDec(self):   # done I think
        ## strucutre ##
        count = 0
        # 'var' type varName (',' varName)* ';'
        self.nextToken()    # var
        typethis = self.type()         # type
        varname = self.varName()      # varname
        self.locals.append([varname, typethis])

        count += 1
        while(self.Rtokens[0] == ","):
            self.nextToken()    # ,
            varname = self.varName()      # varname
            count += 1
            self.locals.append([varname, typethis])

        self.eatToken(";")
        print(self.locals)
        return count

    def varName(self):
        returnme = self.Rtokens[0]
        self.nextToken()
        return returnme

    def subroutineName(self):
        self.subroutineNames.append(self.Rtokens[0])
        self.nextToken()

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
            pass
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
        self.nextToken()      # let
        varname = self.varName()      # varName

        if self.Rtokens[0] == "[":
            self.wrapBody("[", "]", self.expression)
        if self.Rtokens[0] == "=":
            self.wrapBody("=", ";", self.expression)
            self.vm += f"pop {self.findLocal(varname)}\n"
            self.vm += "push local 1\n"
        else:
            print("things ain't adding up here")
            time.sleep(3)
            print("ahh I see, somethings up with the = sign in this let statement")
            raise

    def ifStatement(self):
        ## strucutre ##
        # 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?

        self.nextToken()  # if

        self.wrapBody("(", ")", self.expression)

        self.eatToken("{")
        self.Statements()
        self.eatToken("}")

        if self.Rtokens[0] == "else":
            self.nextToken()
            self.eatToken("{")
            self.Statements()
            self.eatToken("}")
        elif self.nextIsStatement or self.Rtokens[0] == "}":
            return
        else:
            print("invalid if statement")
            raise

    def whileStatement(self):
        ## strucutre ##
        # 'while' '(' expression ')' '{' statements '}'
        self.nextToken()      # let

        self.wrapBody("(", ")", self.expression)

        self.eatToken("{")
        self.Statements()           # statements block
        self.eatToken("}")

    def doStatement(self):
        ## strucutre ##
        # 'do' subroutineCall ';'

        self.nextToken()      # do

        self.subroutineCall()

        self.vm += f"pop temp 0\n"

        self.eatToken(";")  # ;

    def returnStatement(self):
        ## strucutre ##
        # 'return' expression? ';'

        self.nextToken()      # return

        if self.Rtokens[0] == ";":
            self.nextToken()
            return
        else:
            self.expression()   # this will handle exceptions
            if self.Rtokens[0] == ";":
                self.nextToken()  # ;

    ##########################
    ## Identifier Funcitons ##
    ##########################

    def expression(self):
        ## strucutre ##
        # term (op term)*
        self.term()

        while self.Rtokens[0] in self.op:
            thing = self.Rtokens[0]
            self.nextToken()
            self.term()
            if thing == "*":
                self.vm += f"call Math.multiply 2\n"
            elif thing == "+":
                self.vm += f"add\n"
            elif thing == "-":
                self.vm += f"sub\n"

    def term(self):
        ## strucutre ##
        # integerConstant | stringConstant | keywordConstant | varName |
        # varName '[' expression ']' | subroutineCall | '(' expression ')' |
        # unaryOp term

        if self.Rtokens[0] in self.unaryOp:
            self.nextToken()  # this handles the unary op stuff
            self.term()

        elif self.Rtokens[0] in self.KeywordConstant:
            self.nextToken()

        elif "integerConstant" in self.RlexLabels[0]:
            self.vm += f"push constant {self.Rtokens[0]}\n"
            self.nextToken()

        elif "stringConstant" in self.RlexLabels[0]:
            self.vm += f"push constant {len(self.Rtokens[0])}\n"
            self.vm += f"call String.new 1\n"
            for letter in self.Rtokens[0]:
                self.vm += f"push constant {ord(letter)}\n"
                self.vm += f"call String.appendChar 2\n"
            self.nextToken()

        elif "Constant" in self.RlexLabels[0]:
            self.nextToken()

        elif self.Rtokens[1] == "[":
            # print("3")
            self.nextToken()
            self.eatToken("[")
            self.expression()
            if self.Rtokens[0] == "]":
                self.nextToken()
            else:
                print("umm error in term prolly missing end bracket ]")
                raise

        elif self.Rtokens[0] == "(":
            self.wrapBody("(", ")", self.expression)

        elif self.isVarName():
            self.nextToken()
            if self.Rtokens[0] == '[':  # is this 1 or 0?
                self.wrapBody("[", "]", self.expression)

        elif self.Rtokens[1] in [".", "("]:
            self.subroutineCall()
        else:
            print("invalid term expression")
            raise

    def subroutineCall(self):
        ## strucutre ##
        # subroutineName '(' expressionList ')' | (className |
        # varName) '.' subroutineName '(' expressionList ')'
        classthing = ""
        if self.Rtokens[1] == ".":
            classthing = self.Rtokens[0] + "."
            self.nextToken()  # classname or varname
            self.nextToken()  # .

        subthing = self.Rtokens[0]
        self.nextToken()  # subroutinename
        if (self.Rtokens[0] != "("):
            print("what the hell")
            raise

        paramCount = self.wrapBody("(", ")", self.expressionList)

        self.vm += f"call {classthing}{subthing} {paramCount}\n"

    def expressionList(self):
        ## strucutre ##
        # (expression (',' expression)* )?

        if self.Rtokens[0] == ")":
            return 0

        self.expression()

        counter = 1
        while(self.Rtokens[0] == ","):
            counter += 1
            self.nextToken()
            self.expression()

        return counter
