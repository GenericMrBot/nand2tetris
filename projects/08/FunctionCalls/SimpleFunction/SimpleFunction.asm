
 //['function', 'SimpleFunction.test', '2']  
(SimpleFunction.test)
@2
D=A+1
@R15
M=D
(SimpleFunction.test_loop)
@R15
M=M-1
D=M
@SimpleFunction.test_end
D;JEQ
@0
D=A
@SP
M=M+1
A=M-1
M=D
@SimpleFunction.test_loop
0;JMP
(SimpleFunction.test_end)

 //['push', 'local', '0']  

@LCL
D=M
@0
A=D+A
D=M

@SP
M=M+1
A=M-1
M=D

 //['push', 'local', '1']  

@LCL
D=M
@1
A=D+A
D=M

@SP
M=M+1
A=M-1
M=D

 //['add']  

@SP
AM=M-1
D=M
A=A-1
M=M+D

 //['not']  

@SP
A=M-1
M=!M

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

 //['add']  

@SP
AM=M-1
D=M
A=A-1
M=M+D

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
