import socket
import tqdm
import os
import argparse
from sys import argv, exit

def message_error():
	print("Please, use the following format:\n")
	print("python3 your_script.py file domain-name|ip-address port-number\n")
	print("Example: python3 send_file.py meme.png your_vps.ru 8800")

# check that user pass 3 arguments and the file exists
try:
	filename = argv[1]
	host = argv[2]
	port = int(argv[3])
except (NameError, IndexError):
	message_error()
	exit(1)


# check is it possible to connect to server via host and port
try:
	s = socket.socket()
	s.connect((host, port))
except ConnectionRefusedError:
	message_error()
	exit(1)

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B",
unit_scale=True, unit_divisor=1024)

filesize = os.path.getsize(filename)
separator = <SEPARATOR>
s.send(f"{filename}{separator}{filesize}".encode())

f = open(filename, "rb")

# print to console the current progress
for _ in progress:
	bytes_read = f.read(1024)
	if not bytes_read:
		break
	s.sendall(bytes_read)
	progress.update(len(bytes_read))

f.close()
s.close()