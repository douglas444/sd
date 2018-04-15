import multiprocessing;
import socket;
import _thread;
import queue;

received_commands = multiprocessing.Queue();

def config_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    host = socket.gethostname();
    port = read_port();
    s.bind((host,port));
    return s

def store_and_process():
    while True:
        if (received_commands.qsize() > 0):
            command = received_commands.get();
            store(command);
        stored_command = get_stored_command();

        if (stored_command != None):
            process(stored_command);
            unstore(stored_command);

def store(command):
    storage_file = open('data', 'a');
    storage_file.write(command + '\n');
    storage_file.close();

def process(command):
    print('Comando ', command, ' processado com sucesso');

def unstore(command):
    storage_file = open('data', 'r+');
    file_content = storage_file.read();
    storage_file.close();

    stored_commands = file_content.split('\n');
    stored_commands.remove(command);
    file_content = '\n'.join(stored_commands);

    storage_file = open('data','r+');
    storage_file.write(file_content);
    storage_file.close();

def get_stored_command():
    storage_file = open('data','r+');
    file_content = storage_file.read();
    storage_file.close();

    stored_commands = file_content.split('\n');

    if(file_content and len(stored_commands) > 0):
        return stored_commands[0];
    else:
        return None;

def read_port():
    config_file = open('config-servidor.txt','r');
    port = int(config_file.read().split(':')[1]);
    config_file.close;
    return port;

def main():
    s = config_server();
    _thread.start_new_thread(store_and_process,());
    while(True):
        command, addr = s.recvfrom(12345);
        x = 2;
        received_commands.put(command.decode());

if __name__ == "__main__":
    main();
