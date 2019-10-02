import socket
from threading import Thread
import glob

clients = []

def get_filename(filename):
    """
    returns filename for file to be written according to client info
    and copies of this file on the server
    """
    name, ext = filename.split('.')
    print(name + ext)
    original = glob.glob(filename)
    if len(original) == 0:
        return filename
    # finds all the copies using regular expressions
    copies = glob.glob('{}_copy*[0-9].{}'.format(name, ext))
    return '{}_copy{}.{}'.format(name, len(copies)+1, ext)

# Thread to listen one particular client
class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    # clean up
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        # first 1024 bytes are used for the filename
        data = self.sock.recv(1024)
        filename = ''
        # first data part is for name of the file
        # get filename
        if data:
            filename = data.decode('ascii')
            # delete useless symbols
            filename = filename.rstrip('\x00')
        else:
            print('no data is given')
            self._close()
            return
        new_filename = get_filename(filename)
        print('file "{}" will be written as "{}"'.format(filename, new_filename))
        with open(new_filename, 'wb') as f:
            # just write chunks of data one by one
            while True:
                # try to read 1024 bytes from user
                # this is blocking call, thread will be paused here
                data = self.sock.recv(1024)
                if data:
                    f.write(data)
                else:
                    # no data anymore
                    self._close()
                    # finish the thread
                    return


def main():
    next_name = 1

    # AF_INET – IPv4, SOCK_STREAM – TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse address; in OS address will be reserved after app closed for a while
    # so if we close and imidiatly start server again – we'll get error
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # listen to all interfaces at 8800 port
    sock.bind(('', 8800))
    sock.listen()
    while True:
        # blocking call, waiting for new client to connect
        con, addr = sock.accept()
        clients.append(con)
        name = 'u' + str(next_name)
        next_name += 1
        print(str(addr) + ' connected as ' + name)
        # start new thread to deal with client
        ClientListener(name, con).start()


if __name__ == "__main__":
    main()
