import sys
import socket
import time
import argparse
import ipaddress

def netcat(ip, port, content, timeout):
    try:
        print(f'Sending job to {ip}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.sendall(content.encode('utf-8'))
        sock.shutdown(socket.SHUT_WR)
        sock.close()
        print(f'Connection to {ip} closed')
    except ConnectionRefusedError:
        print(f'Connection refused by {ip}')
    except TimeoutError:
        print(f'Timeout for {ip}')
    except:
        print(f'something went wrong with {ip}')


def main():
    content = "test text\n"
    port = 9100
    timeout = 1

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--Port", help = "Port to use, default 9100")
    parser.add_argument("-f", "--HostFile", help = "File with ips of printers, separetad by commas, no spaces")
    parser.add_argument("-tg", "--Target", help = "Single ip of a printer to use instead of a file")
    parser.add_argument("-t", "--Text", help = "Text to send")
    parser.add_argument("-sn", "--Subnet", help = "Send print jobs to every printer on a local subnet (For Example: 255.255.255.0 or /24)")
    parser.add_argument("-ip", "--NetIp", help = "overwrite local ip used for subnet")
    parser.add_argument("-to", "--Timeout", help = "Set request timeout")
    args = parser.parse_args()

    if not args.Target and not args.HostFile:
        print("Please provide ips")

    if args.Port:
        port = args.Port

    if args.Text:
        content = args.Text
    
    if args.Timeout:
        timeout = float(args.Timeout)

    if args.Target:
        print('using list of ips')
        for ip in args.Target.split(","):
            netcat(ip, port, content)

    if args.HostFile:
        print('using a file of ips')
        with open(args.HostFile, 'r') as ip_file:
            for ip in ip_file:
                netcat(ip.strip(), port, content)
    
    if args.Subnet:
        mask = args.Subnet
        print(f'using subnet mask {mask}')
        if args.NetIp:
            sub_ip = args.NetIp
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            print(s.getsockname()[0])
            sub_ip = s.getsockname()[0]
            s.close()
        print(f'using local ip {sub_ip}')
        if '.' in mask:
            mask = '/' + mask
        for ip in ipaddress.ip_network(sub_ip+mask, False).hosts():
            netcat(str(ip), port, content, timeout)

        


if __name__ == "__main__":
    main()