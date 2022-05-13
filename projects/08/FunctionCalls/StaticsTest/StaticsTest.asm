@256
D=A
@SP
M=D
@return_address0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(return_address0)

 //['function', 'Sys.init', '0']  
(Sys.init)
@0
D=A+1
@R15
M=D
(Sys.init_loop)
@R15
M=M-1
D=M
@Sys.init_end
D;JEQ
@0
D=A
@SP
M=M+1
A=M-1
M=D
@Sys.init_loop
0;JMP
(Sys.init_end)

 //['push', 'constant', '6']  
@6
D=A
@SP
M=M+1
A=M-1
M=D

 //['push', 'constant', '8']  
@8
D=A
@SP
M=M+1
A=M-1
M=D

 //['call', 'Class1.set', '2']  
@return_address4
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(return_address4)

 //['pop', 'temp', '0']  

@5
D=A
@0
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'constant', '23']  
@23
D=A
@SP
M=M+1
A=M-1
M=D

 //['push', 'constant', '15']  
@15
D=A
@SP
M=M+1
A=M-1
M=D

 //['call', 'Class2.set', '2']  
@return_address8
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(return_address8)

 //['pop', 'temp', '0']  

@5
D=A
@0
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['call', 'Class1.get', '0']  
@return_address10
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(return_address10)

 //['call', 'Class2.get', '0']  
@return_address11
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(return_address11)

 //['label', 'WHILE']  
(Class2.get$WHILE)

 //['goto', 'WHILE']  
@Class2.get$WHILE
0;JMP

 //['function', 'Class1.set', '0']  
(Class1.set)
@0
D=A+1
@R15
M=D
(Class1.set_loop)
@R15
M=M-1
D=M
@Class1.set_end
D;JEQ
@0
D=A
@SP
M=M+1
A=M-1
M=D
@Class1.set_loop
0;JMP
(Class1.set_end)

 //['push', 'argument', '0']  

@ARG
D=M
@0
A=D+A
D=M

@SP
M=M+1
A=M-1
M=D

 //['pop', 'static', '0']  

@Class1.0
D=A
@0
D=D

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'argument', '1']  

@ARG
D=M
@1
A=D+A
D=M

@SP
M=M+1
A=M-1
M=D

 //['pop', 'static', '1']  

@Class1.1
D=A
@1
D=D

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'constant', '0']  
@0
D=A
@SP
M=M+1
A=M-1
M=D

 //['return']  
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
A=M-1
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP

 //['function', 'Class1.get', '0']  
(Class1.get)
@0
D=A+1
@R15
M=D
(Class1.get_loop)
@R15
M=M-1
D=M
@Class1.get_end
D;JEQ
@0
D=A
@SP
M=M+1
A=M-1
M=D
@Class1.get_loop
0;JMP
(Class1.get_end)

 //['push', 'static', '0']  
@Class1.0
D=M

@SP
M=M+1
A=M-1
M=D

 //['push', 'static', '1']  
@Class1.1
D=M

@SP
M=M+1
A=M-1
M=D

 //['sub']  

@SP
AM=M-1
D=M
A=A-1
M=M-D

 //['return']  
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
A=M-1
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP

 //['function', 'Class2.set', '0']  
(Class2.set)
@0
D=A+1
@R15
M=D
(Class2.set_loop)
@R15
M=M-1
D=M
@Class2.set_end
D;JEQ
@0
D=A
@SP
M=M+1
A=M-1
M=D
@Class2.set_loop
0;JMP
(Class2.set_end)

 //['push', 'argument', '0']  

@ARG
D=M
@0
A=D+A
D=M

@SP
M=M+1
A=M-1
M=D

 //['pop', 'static', '0']  

@Class2.0
D=A
@0
D=D

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'argument', '1']  

@ARG
D=M
@1
A=D+A
D=M

@SP
M=M+1
A=M-1
M=D

 //['pop', 'static', '1']  

@Class2.1
D=A
@1
D=D

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'constant', '0']  
@0
D=A
@SP
M=M+1
A=M-1
M=D

 //['return']  
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
A=M-1
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP

 //['function', 'Class2.get', '0']  
(Class2.get)
@0
D=A+1
@R15
M=D
(Class2.get_loop)
@R15
M=M-1
D=M
@Class2.get_end
D;JEQ
@0
D=A
@SP
M=M+1
A=M-1
M=D
@Class2.get_loop
0;JMP
(Class2.get_end)

 //['push', 'static', '0']  
@Class2.0
D=M

@SP
M=M+1
A=M-1
M=D

 //['push', 'static', '1']  
@Class2.1
D=M

@SP
M=M+1
A=M-1
M=D

 //['sub']  

@SP
AM=M-1
D=M
A=A-1
M=M-D

 //['return']  
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
A=M-1
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
