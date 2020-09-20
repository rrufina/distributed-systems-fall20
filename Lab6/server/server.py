
import socket
import tqdm
import os
from threading import Thread

host = "3.17.60.139" # 0.0.0.0 to run on localhost
port = 5050
separator = "<SEPARATOR>"

# thread for a client
class ClientThread(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name    
    def run(self):
        # read data from client
        received = self.sock.recv(1024).decode()
        filename, filesize = received.split(separator)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        # change file name in case name collision 
        filename = check_collisions(filename)

        # print to console the current progress
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        f = open(filename, "wb")
        for _ in progress:
            bytes_read = self.sock.recv(1024)
            f.write(bytes_read)
            progress.update(len(bytes_read))
        f.close()

# check name collisions, change name if the file exists
def check_collisions(name):
    root, ext = os.path.splitext(name)
    if os.path.exists(f'./{name}'):
        copy = 1
        while os.path.exists(f'./{root}_copy{copy}{ext}'):
            copy += 1
        new_name = f'{root}_copy{copy}{ext}'
        return new_name
    else:
        return name

# create the server socket and bind it
s = socket.socket()
s.bind(('', port))
print(f'Listen {host}:{port}')

while True:
    s.listen(1)
    # accept connection if there is any and create a thread for this connection
    client_socket, address = s.accept()
    newthread = ClientThread(address, client_socket)
    newthread.start()

client_socket.close()
s.close()