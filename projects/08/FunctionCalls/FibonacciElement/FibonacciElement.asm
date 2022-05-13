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

 //['push', 'constant', '4']  
@4
D=A
@SP
M=M+1
A=M-1
M=D

 //['call', 'Main.fibonacci', '1']  
@return_address3
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
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return_address3)

 //['label', 'WHILE']  
(Main.fibonacci$WHILE)

 //['goto', 'WHILE']  
@Main.fibonacci$WHILE
0;JMP

 //['function', 'Main.fibonacci', '0']  
(Main.fibonacci)
@0
D=A+1
@R15
M=D
(Main.fibonacci_loop)
@R15
M=M-1
D=M
@Main.fibonacci_end
D;JEQ
@0
D=A
@SP
M=M+1
A=M-1
M=D
@Main.fibonacci_loop
0;JMP
(Main.fibonacci_end)

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

 //['push', 'constant', '2']  
@2
D=A
@SP
M=M+1
A=M-1
M=D

 //['lt']  

@SP
A=M-1
D=M
A=A-1
D=D-M
@zero.4
D;JGT
@end.4
D=0;JMP
(zero.4)
D=-1
(end.4)
@SP
AM=M-1
A=A-1
M=D

 //['if-goto', 'IF_TRUE']  
@SP
AM=M-1
D=M
@Main$IF_TRUE
D;JNE

 //['goto', 'IF_FALSE']  
@Main$IF_FALSE
0;JMP

 //['label', 'IF_TRUE']  
(Main$IF_TRUE)

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

 //['label', 'IF_FALSE']  
(Main$IF_FALSE)

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

 //['push', 'constant', '2']  
@2
D=A
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

 //['call', 'Main.fibonacci', '1']  
@return_address14
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
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return_address14)

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

 //['push', 'constant', '1']  
@1
D=A
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

 //['call', 'Main.fibonacci', '1']  
@return_address18
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
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return_address18)

 //['add']  

@SP
AM=M-1
D=M
A=A-1
M=M+D

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
