import socket
import sys
import time
import errno
import math
from multiprocessing import Process

ok_message = 'HTTP/1.0 200 OK\n\n'
nok_message = 'HTTP/1.0 404 NotFound\n\n'
walcome_message ='Walcome To Saif Calculator....\n\n'+'Operation you can choose:-\n\n'+'1. Log\n\n'+'2. Square Root\n\n'+'3. Expontential Function\n\n'
how_message = '\nInsert only log <base> <number> for log\n\n'+'Insert sqrt/exp <number> for square root and expontential\n' + 'Example: log 2 36, sqrt 3 or exp 36\n'+ 'Number = '                
error_message = '\n\nError input!!\nDo you want to continue or not(Y/n):'
ask_message = '\nDo you want to continue or not(Y/n):'


def process_start(s_sock):
    
  
    while True:
        s_sock.send(str.encode(walcome_message + how_message))
        data = s_sock.recv(2048)
        data = data.decode("utf-8")
        #data = data.split()
        #siz = len(data)
        #op = str(data[0])
        #num = str(data[2])
        #base = str(data[1])
        
        
        data = data.split()
        op = data[0]
        
        if op == 'log':
            num = float(data[2])
            base = int(data[1])
            answer = math.log(num,base)
            result = str(op) + str(base) + " " + str(num) +  "= " + str(answer)
            
        elif op == 'sqrt':
            num = int(data[1])
            answer = math.sqrt(num)
            result = str(op) + str(num) +  "= " + str(answer) 
            
        elif op == 'exp':
            num = float(data[1])
            answer = math.exp(num)
            result = str(op) + str(num) +  "= " + str(answer)  
                
        elif op == 'n':
            continue
            
        else:
            print('Error input')
            result = error_message
            
          
        s_sock.send(str.encode(result + '\n\n' + ask_message))
        ans = s_sock.recv(2048)
        ans = ans.decode("utf-8")
        ans = str(ans)
        if ans == 'Y':
           continue
        
        #siz= str(siz)
        #s_sock.send(str.encode(op+num+base))
     
    s_sock.close()


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",8888))
    print("listening...")
    s.listen(3)
    try:
        while True:
            try:
                s_sock, s_addr = s.accept()
                p = Process(target=process_start, args=(s_sock,))
                p.start()

            except socket.error:

                print('got a socket error')

    except Exception as e:        
        print('an exception occurred!')
        print(e)
        sys.exit(1)
    finally:
     	   s.close()
