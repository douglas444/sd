import socket;

def config_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    host = socket.gethostname();
    port = read_port();
    return s,host,port;

def read_port():
    config_file = open('config-servidor.txt','r');
    port = int(config_file.read().split(':')[1]);
    config_file.close();
    return port;

def main():
    s,host,port = config_server();
    while True:
    	data = input("Entre com um comando: ");
    	s.sendto(data.encode(), (host, port));

if __name__ == "__main__":
    main();
