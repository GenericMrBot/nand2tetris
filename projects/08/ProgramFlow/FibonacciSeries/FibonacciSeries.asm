
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

 //['pop', 'pointer', '1']  

@3
D=A
@1
D=D+A

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

 //['pop', 'that', '0']  

@THAT
D=M
@0
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'constant', '1']  
@1
D=A
@SP
M=M+1
A=M-1
M=D

 //['pop', 'that', '1']  

@THAT
D=M
@1
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

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

 //['pop', 'argument', '0']  

@ARG
D=M
@0
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['label', 'MAIN_LOOP_START']  
(FibonacciSeries$MAIN_LOOP_START)

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

 //['if-goto', 'COMPUTE_ELEMENT']  
@SP
AM=M-1
D=M
@FibonacciSeries$COMPUTE_ELEMENT
D;JNE

 //['goto', 'END_PROGRAM']  
@FibonacciSeries$END_PROGRAM
0;JMP

 //['label', 'COMPUTE_ELEMENT']  
(FibonacciSeries$COMPUTE_ELEMENT)

 //['push', 'that', '0']  

@THAT
D=M
@0
A=D+A
D=M

@SP
M=M+1
A=M-1
M=D

 //['push', 'that', '1']  

@THAT
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

 //['pop', 'that', '2']  

@THAT
D=M
@2
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'pointer', '1']  

@3
D=A
@1
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

 //['add']  

@SP
AM=M-1
D=M
A=A-1
M=M+D

 //['pop', 'pointer', '1']  

@3
D=A
@1
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

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

 //['pop', 'argument', '0']  

@ARG
D=M
@0
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['goto', 'MAIN_LOOP_START']  
@FibonacciSeries$MAIN_LOOP_START
0;JMP

 //['label', 'END_PROGRAM']  
(FibonacciSeries$END_PROGRAM)
