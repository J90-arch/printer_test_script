import sys
import socket
import time

hosts_file = sys.argv[1]
port = 9100

def numLines():
    with open(hosts_file) as f:
        line_count = 0
        for line in f:
            line_count += 1
    return line_count

def netcat(hn, p, c):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hn, p))

    sock.sendall(c)
    sock.shutdown(socket.SHUT_WR)

    print("CONNECTION CLOSED")
    sock.close()

def processFile(file, c):
    i = 0
    while i<numLines():
        netcat(file.readline().rstrip(), port, c)
        i+=1


content = "text\n" #change this to what you want to print

hfile = open(hosts_file, "r")
processFile(hfile, content.encode())

hfile.close()