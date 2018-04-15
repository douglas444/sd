import socket;
import _thread;
import time;
Comandos = ['CREATE', 'READ', 'UPDATE', 'DELETE'];
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
def console(s,host,port):
    while True:
        data = input("entre com um comando: ");
        comando = data.split(' ');
        if(comando[0] in Comandos):
            chave_valor = comando[1].split(',');
            chave = comando[0][1:];
            valor = comando[1][:-1];
            s.sendto(data.encode(), (host, port));
        else:
            print("comando invalido");

def main():
    s,host,port = config_server();
    _thread.start_new_thread(console,(s,host,port));
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main();
