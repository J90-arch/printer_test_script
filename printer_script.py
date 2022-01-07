import sys
import socket
import time
import argparse

def netcat(ip, port, content):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.sendall(content.encode('utf-8'))
        sock.shutdown(socket.SHUT_WR)
        sock.close()
        print(f'Connection to {ip} closed')
    except ConnectionRefusedError:
        print(f'Connection refused by {ip}')
    except:
        print(f'something went wrong with {ip}')


def main():
    content = "test text\n"
    port = 9100

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--Port", help = "Port to use, default 9100")
    parser.add_argument("-f", "--HostFile", help = "File with ips of printers, separetad by commas, no spaces")
    parser.add_argument("-x", "--Target", help = "Single ip of a printer to use instead of a file")
    parser.add_argument("-t", "--Text", help = "Text to send")
    args = parser.parse_args()

    if args.Target and args.HostFile:
        print("Use single ip OR a list of ips in a file!")
        exit()

    if not args.Target and not args.HostFile:
        print("Please provide ips")

    if args.Port:
        port = args.Port

    if args.Text:
        content = args.Text
    
    if args.Target:
        for ip in args.Target.split(","):
            netcat(ip, port, content)

    if args.HostFile:
        with open(args.HostFile, 'r') as ip_file:
            for ip in ip_file:
                netcat(ip.strip(), port, content)

if __name__ == "__main__":
    main()