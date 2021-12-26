import socket
import sys
import time
import errno
import math
from multiprocessing import Process

ok_message = 'HTTP/1.0 200 OK\n\n'
nok_message = 'HTTP/1.0 404 NotFound\n\n'
welcome_message = 'Walcome To Saif Calculaotor...\n\n' + 'Operation you can choose:-\n1. Log\n2. Square Root\n3. Expontential'
how_message = 'How to use....\n\nInsert only log <base> <number> for log\nExample: log 2 39\n\nInsert sqrt/exp <number> for square root and expontential\nExample sqrt/exp 78.0\n\n' 
ask_message = 'Do you want to continue(Y/n)'

def process_start(s_sock):
    
    while True:
        s_sock.send(str.encode(welcome_message + how_message + '\nNumber = '))
        data = s_sock.recv(2048)
        data = data.decode("utf-8")
        data = data.split()
        op = str(data[0])
      
        
        if op == 'log':
            base = int(data[1])
            num = float(data[2])
            answer = math.log(num,base)
            result = str(op) + str(base) + " " + str(num) + "= " + str(answer)
        
        elif op == 'sqrt':
            num = float(data[1])
            answer = math.sqrt(num)
            result = str(op) + " " + str(num) + "= " + str(answer)
        
        elif op == 'exp':
            num = float(data[1])
            answer = math.exp(num)
            result = str(op) + " " + str(num) + "= " + str(answer)
            
        else:
            result = 'Error Input!!!'
        
        s_sock.send(str.encode(result + '\n\n'+ ask_message))
        
       
        
        ask = s_sock.recv(2048)
        ask = str(ask)
        if ask == 'Y':
            continue
        
        
        
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
