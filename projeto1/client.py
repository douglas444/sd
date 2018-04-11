import socket;

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);

host = socket.gethostname();
port = 12345;

while True:
	data = input("Entre com um comando: ");
	s.sendto(data.encode(), (host, port));
