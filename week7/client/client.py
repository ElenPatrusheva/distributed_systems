import sys
from tqdm import tqdm
import socket
import os
import math


def send_file(filename, address, serv_port):
    serv_host = socket.gethostbyname(address)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((serv_host, serv_port))
    sock.sendall(filename.encode())
    empty = '\0'*(1024 - len(filename.encode()))
    sock.sendall(empty.encode())
    with open (filename, 'rb') as f:
        file_size = os.path.getsize(filename)
        for progress in tqdm(range(math.ceil(file_size/1024))):
            part = f.read(1024)
            sock.sendall(part)
    sock.close()

def main():
    if len(sys.argv) < 4:
        print('Only {} arguments are given'.format(len(argv)))
        return
    filename = sys.argv[1]
    address = sys.argv[2]
    serv_port = int(sys.argv[3])
    send_file(filename, address, serv_port)

if __name__ == "__main__":
    main()
