import socket;
import _thread;
import time;
import multiprocessing;
import queue;
import sys

results = multiprocessing.Queue();

def config_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    host = socket.gethostname();
    port = read_port();
    return s,host,port;

def read_port():
    config_file = open('server_config','r');
    port = int(config_file.read().split(':')[1]);
    config_file.close();
    return port;

def console(s,host,port):
    while True:
        command = input('> ');
        s.sendto(command.encode(), (host, port))

def main():
    s,host,port = config_server();
    _thread.start_new_thread(console,(s,host,port));
    while True:
        result, addr = s.recvfrom(4096);
        sys.stdout.write('[SERVER MESSAGE] ' + result.decode() + "\n> ")

if __name__ == "__main__":
    main();
