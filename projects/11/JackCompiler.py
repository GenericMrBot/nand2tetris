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
from inspect import isclass
import time


class JackCompiler:
    def __init__(self, tokens, lexLabels, file, classNames):
        self.tokens = tokens
        self.Rtokens = tokens       # stands for remaining tokens
        self.lexLabels = lexLabels
        self.RlexLabels = lexLabels  # remaining labels to be added to xml
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
        self.whilecount = 0
        self.ifcount = 0
        self.statics = []
        self.fields = []
        self.arguments = []
        self.locals = []
        self.methods = []

    def writeVM(self):
        filename = self.file
        filename = filename.removesuffix(".jack")
        with open(f"{filename}.vm", "w") as thing:
            thing.write(self.vm)              # write to file
        print(f"{self.filename}.vm contains the assembly translation")

    def nextToken(self):
        returnme = self.Rtokens[0]
        self.Rtokens = self.Rtokens[1:]
        self.RlexLabels = self.RlexLabels[1:]
        return returnme

    def eatToken(self, list):
        # helper func
        if self.Rtokens[0] in list:
            self.nextToken()
            return self.Rtokens[0]
        else:
            print(f"Expected {list} got {self.Rtokens[0]}")
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

    def WhileCount(self):
        self.whilecount += 1
        return self.whilecount - 1

    def IfCount(self):
        self.ifcount += 1
        return self.ifcount - 1

    ##########################
    ## Symbol Table Helpers ##
    ##########################

    def isVarName(self):
        inLCL = [self.Rtokens[0] == i[0] for i in self.locals]
        inARG = [self.Rtokens[0] == i[0] for i in self.arguments]
        inSTC = [self.Rtokens[0] == i[0] for i in self.statics]
        inFLD = [self.Rtokens[0] == i[0] for i in self.fields]
        if any(inLCL):
            return
        return False

    def getVarVMName(self, varname):
        for i, e in enumerate(self.locals):
            if e[0] == varname:
                return f"local {i}"

        for i, e in enumerate(self.arguments):
            if e[0] == varname:
                return f"argument {i}"

        for i, e in enumerate(self.fields):
            if e[0] == varname:
                return f"this {i}"

        for i, e in enumerate(self.statics):
            if e[0] == varname:
                return f"static {i}"
        print("something went wrong at getVarVMName")
        raise

    def addVar(self, scope, varname, type):
        if scope == "local":
            self.locals.append([varname, type])
        if scope == "argument":
            self.arguments.append([varname, type])
        if scope == "field":
            self.fields.append([varname, type])
        if scope == "static":
            self.statics.append([varname, type])

    def isVar(self, varname):
        for e in self.locals:
            if e[0] == varname:
                return True

        for e in self.arguments:
            if e[0] == varname:
                return True

        for e in self.fields:
            if e[0] == varname:
                return True

        for e in self.statics:
            if e[0] == varname:
                return True

        return False

    def getclassname(self, varname):
        for e in self.locals:
            if e[0] == varname:
                return e[1]

        for e in self.arguments:
            if e[0] == varname:
                return e[1]

        for e in self.fields:
            if e[0] == varname:
                return e[1]

        for e in self.statics:
            if e[0] == varname:
                return e[1]

        return False

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

        self.eatToken("class")  # class key word
        self.nextToken()        # class name
        self.nextToken()        # {

        # classVarDec*
        num_class_vars = 0
        if not(self.Rtokens[0] in ["function", "method", "constructor"]):
            num_class_vars = self.classVarDec()

        # subroutineDec*
        self.subroutineDec(f"push constant {num_class_vars}\n", num_class_vars)

        self.nextToken()  # {

    def classVarDec(self):
        ## strucutre ##
        # ('static' | 'field') type varName (',' varName)* ';'
        myscope = self.nextToken()      # ('static' | 'field')
        vartype = self.type()           # type
        varname = self.nextToken()      # varName
        self.addVar(myscope, varname, vartype)
        count = 1

        while(self.Rtokens[0] == ","):
            self.nextToken()   # ,
            varname = self.nextToken()      # varName
            self.addVar(myscope, varname, vartype)
            count += 1

        self.eatToken(";")    # ;
        if not(self.Rtokens[0] in ["function", "method", "constructor"]):
            count += self.classVarDec()
        return count

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

    def subroutineDec(self, pushthing, num_class_vars, isMethod=0):
        ## strucutre ##
        # ('constructor' | 'function' | 'method')
        # ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        if self.Rtokens[0] == "method":
            isMethod = 1
            self.methods.append([self.Rtokens[2]])

        self.eatToken(['constructor', 'function', 'method'])

        if self.Rtokens[0] == "void":
            self.nextToken()   # void
            returnme = "push constant 0\n"
        else:
            self.type()
            returnme = ""  # just return the top of the stack

        if "identifier" in self.RlexLabels[0]:
            if self.Rtokens[0] == "new":
                pushthing += f"call Memory.alloc 1\n"

            self.vm += f"function {self.filename}.{self.Rtokens[0]}"
            self.nextToken()
        else:
            print(f"{self.Rtokens[0]} is not an identifier")
            raise

        # '(' parameterList ')'
        num_params = self.wrapBody("(", ")", self.paramList)

        self.subroutineBody(pushthing, num_class_vars)

        # idk if this is right
        self.vm += f"{returnme}"
        self.vm += f"return\n"

        self.whilecount = 0
        self.ifcount = 0

        if self.Rtokens[0] in ['function', 'method']:
            self.subroutineDec(f"push argument 0\n", num_class_vars)

    def paramList(self):
        ## strucutre ##
        # ((type varName) (',' type varName)*)?
        count = 0
        if self.Rtokens[0] == ")":
            return count

        mytype = self.type()
        myvar = self.nextToken()
        self.addVar("argument", myvar, mytype)
        count += 1

        while (self.Rtokens[0] == ","):
            self.nextToken()    # ,
            mytype = self.type()
            myvar = self.nextToken()
            self.addVar("argument", myvar, mytype)
            count += 1

        return count

    def subroutineBody(self, pushthing, num_params):
        ## strucutre ##
        # '{' varDec* statements '}'

        # opening {
        self.eatToken("{")

        num_func_vars = self.varDecs()      # varDec*

        # number at end of func decs
        self.vm += f" {num_func_vars}\n"

        self.vm += pushthing
        self.vm += f"pop pointer 0\n"

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
        varname = self.nextToken()      # varname
        self.locals.append([varname, typethis])

        count += 1
        while(self.Rtokens[0] == ","):
            self.nextToken()    # ,
            varname = self.nextToken()      # varname
            self.locals.append([varname, typethis])
            count += 1

        self.eatToken(";")
        return count

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
        self.nextToken()      #
        # self.vm += "start let\n"
        saveme = self.getVarVMName(self.Rtokens[0])
        varname = self.nextToken()      # varName

        ending = ""

        if self.Rtokens[0] == "[":
            self.wrapBody("[", "]", self.expression)
            self.vm += f"push {saveme}\n"
            self.vm += "add\n"
            ending = "pop temp 0\npop pointer 1\npush temp 0\npop that 0\n"
        else:
            thing = self.getVarVMName(varname)
            ending += f"pop {thing}\n"
        if self.Rtokens[0] == "=":
            self.wrapBody("=", ";", self.expression)
            # not supposed to be here when a = array.new(thing)
            # self.vm += f"push {thing}\n"
        else:
            print("things ain't adding up here")
            time.sleep(3)
            print("ahh I see, somethings up with the = sign in this let statement")
            raise

        self.vm += ending
        # self.vm += "end let\n"

    def ifStatement(self):
        ## strucutre ##
        # 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?

        # self.vm += "ifStatement\n"

        self.nextToken()  # if

        self.wrapBody("(", ")", self.expression)

        count = self.IfCount()

        # self.vm += "eq\n"
        self.vm += f"if-goto IF_TRUE{count}\n"
        self.vm += f"goto IF_FALSE{count}\n"
        self.vm += f"label IF_TRUE{count}\n"

        self.eatToken("{")
        self.Statements()
        self.eatToken("}")

        self.vm += f"label IF_FALSE{count}\n"

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
        thing = self.WhileCount()
        self.vm += f"label WHILE_EXP{thing}\n"

        self.wrapBody("(", ")", self.expression)

        self.vm += f"if-goto WHILE_END{thing}\n"

        self.eatToken("{")
        self.Statements()           # statements block
        self.eatToken("}")
        self.vm += f"goto WHILE_EXP{thing}\n"
        self.vm += f"label WHILE_END{thing}\n"

    def doStatement(self):
        ## strucutre ##
        # 'do' subroutineCall ';'

        # self.vm += "________________\n"

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
            if thing == "<":
                self.vm += f"lt\n"
                # self.vm += f"not\n"
            elif thing == ">":
                self.vm += f"gt\n"
                # self.vm += f"not\n"
            elif thing == "=":
                self.vm += f"eq\n"
            elif thing == "*":
                self.vm += f"call Math.multiply 2\n"
            elif thing == "/":
                self.vm += f"call Math.divide 2\n"
            elif thing == "+":
                self.vm += f"add\n"
            elif thing == "-":
                self.vm += f"sub\n"
            elif thing == "&":
                self.vm += f"and\n"

    def term(self):
        ## strucutre ##
        # integerConstant | stringConstant | keywordConstant | varName |
        # varName '[' expression ']' | subroutineCall | '(' expression ')' |
        # unaryOp term

        # print(self.Rtokens[0])

        if self.isVar(self.Rtokens[0]):
            thing = self.Rtokens[0]
            self.nextToken()
            ending = f"push {self.getVarVMName(thing)}\n"
            if self.Rtokens[0] == '[':  # is this 1 or 0?
                self.wrapBody("[", "]", self.expression)
                ending += f"add\n"
                ending += f"pop pointer 1\n"
                ending += f"push that 0\n"

            self.vm += ending

        elif self.Rtokens[0] in self.unaryOp:
            # this handles the unary op stuff
            self.nextToken()
            self.term()

        elif self.Rtokens[0] in self.KeywordConstant:
            thing = self.nextToken()
            if thing == "this":
                self.vm += f"push pointer 0\n"
            elif thing == "that":
                self.vm += f"push pointer 1\n"
            elif thing == "true":
                self.vm += f"push constant 0\nnot\n"
            elif thing == "false":
                self.vm += f"push constant 0\n"

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

        elif self.Rtokens[0] == "(":
            # '(' expression ')'
            self.wrapBody("(", ")", self.expression)

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
        paramCount = 0
        if not(self.Rtokens[1] == "."):
            paramCount = 1
            self.vm += "push pointer 0\n"
            classthing = self.filename + "."
        elif self.isVar(self.Rtokens[0]):
            paramCount = 1
            self.vm += f"push {self.getVarVMName(self.Rtokens[0])}\n"
            classthing = self.getclassname(self.Rtokens[0]) + "."
            self.nextToken()  # classname
            self.nextToken()  # .
        else:
            classthing = self.Rtokens[0] + "."
            self.nextToken()  # classname
            self.nextToken()  # .

        subthing = self.nextToken()  # subroutinename

        paramCount += self.wrapBody("(", ")", self.expressionList)

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
