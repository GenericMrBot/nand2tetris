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

 //['push', 'constant', '4000']  
@4000
D=A
@SP
M=M+1
A=M-1
M=D

 //['pop', 'pointer', '0']  

@3
D=A
@0
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'constant', '5000']  
@5000
D=A
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

 //['call', 'Sys.main', '0']  
@return_address6
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
@Sys.main
0;JMP
(return_address6)

 //['pop', 'temp', '1']  

@5
D=A
@1
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['label', 'LOOP']  
(Sys.main$LOOP)

 //['goto', 'LOOP']  
@Sys.main$LOOP
0;JMP

 //['function', 'Sys.main', '5']  
(Sys.main)
@5
D=A+1
@R15
M=D
(Sys.main_loop)
@R15
M=M-1
D=M
@Sys.main_end
D;JEQ
@0
D=A
@SP
M=M+1
A=M-1
M=D
@Sys.main_loop
0;JMP
(Sys.main_end)

 //['push', 'constant', '4001']  
@4001
D=A
@SP
M=M+1
A=M-1
M=D

 //['pop', 'pointer', '0']  

@3
D=A
@0
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'constant', '5001']  
@5001
D=A
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

 //['push', 'constant', '200']  
@200
D=A
@SP
M=M+1
A=M-1
M=D

 //['pop', 'local', '1']  

@LCL
D=M
@1
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'constant', '40']  
@40
D=A
@SP
M=M+1
A=M-1
M=D

 //['pop', 'local', '2']  

@LCL
D=M
@2
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'constant', '6']  
@6
D=A
@SP
M=M+1
A=M-1
M=D

 //['pop', 'local', '3']  

@LCL
D=M
@3
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'constant', '123']  
@123
D=A
@SP
M=M+1
A=M-1
M=D

 //['call', 'Sys.add12', '1']  
@return_address22
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
@Sys.add12
0;JMP
(return_address22)

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

 //['push', 'local', '2']  

@LCL
D=M
@2
A=D+A
D=M

@SP
M=M+1
A=M-1
M=D

 //['push', 'local', '3']  

@LCL
D=M
@3
A=D+A
D=M

@SP
M=M+1
A=M-1
M=D

 //['push', 'local', '4']  

@LCL
D=M
@4
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

 //['add']  

@SP
AM=M-1
D=M
A=A-1
M=M+D

 //['add']  

@SP
AM=M-1
D=M
A=A-1
M=M+D

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

 //['function', 'Sys.add12', '0']  
(Sys.add12)
@0
D=A+1
@R15
M=D
(Sys.add12_loop)
@R15
M=M-1
D=M
@Sys.add12_end
D;JEQ
@0
D=A
@SP
M=M+1
A=M-1
M=D
@Sys.add12_loop
0;JMP
(Sys.add12_end)

 //['push', 'constant', '4002']  
@4002
D=A
@SP
M=M+1
A=M-1
M=D

 //['pop', 'pointer', '0']  

@3
D=A
@0
D=D+A

@SP
AM=M-1
D=D+M
A=D-M
M=D-A

 //['push', 'constant', '5002']  
@5002
D=A
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

 //['push', 'constant', '12']  
@12
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
