import multiprocessing;
import socket;
import _thread;
import queue;

received_commands = multiprocessing.Queue();
processing_commands = multiprocessing.Queue();

dados = {}

def config_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    host = socket.gethostname();
    port = read_port();
    s.bind((host,port));
    return s

def store_and_log():
    while True:
        if (received_commands.qsize() > 0):
            command = received_commands.get();
            print(str(command[0][0]) + ' ' + str(command[0][1]) + ' ' + command[1]);
            store(str(command[0][0]) + ' ' + str(command[0][1]) + ' ' + command[1]);
            processing_commands.put(command);


def store(command):
    storage_file = open('data', 'a');
    storage_file.write(command + '\n');
    storage_file.close();

def process_commands(s):
    while (True):
        if(processing_commands.qsize() > 0):
            command = processing_commands.get();
            process(command,s);

def process(data,s):
    (client_addr,command) = data;
    print('Comando ', data, ' processado com sucesso');
    command = command.split(' ');
    operation = command[0];
    chave_valor = command[1].split(',');
    chave = chave_valor[0][1:];
    valor = chave_valor[1][:-1];
    response = '';
    if(operation == 'UPDATE'):
        response = update(chave,valor);
    if(operation == 'CREATE'):
        response = create(chave,valor);
    if(operation == 'READ'):
        response = read(chave,valor);
    if(operation == 'DELETE'):
        response = delete(chave,valor);
    s.sendto(response.encode(),client_addr)

def update(chave,valor):
    if(chave in dados):
        dados[chave] = valor;
        return 'valor alterado';
    else:
        return 'chave nao encontrada';

def create(chave,valor):
    if(chave not in dados):
        dados[chave] = valor;
        return 'valor criado';
    else:
        return 'chave ja esta sendo utilizada';

def read(chave,valor):
    if(chave in dados):
        return dados[chave];
    else:
        return 'chave nao encontrada'

def delete(chave,valor):
    if(chave in dados):
        del(dados[chave]);
        return 'deletado com sucesso'
    else:
        return 'chave nao encontrada'

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
    _thread.start_new_thread(store_and_log,());
    _thread.start_new_thread(process_commands,(s,));
    while(True):
        command, addr = s.recvfrom(12345);
        print (addr)
        received_commands.put((addr,command.decode()));

if __name__ == "__main__":
    main();
