import multiprocessing;
import socket;
import _thread;
import queue;
from enum import Enum;
from sys import getsizeof;

KEY_MAX_SIZE = 28;
DATA_MAX_SIZE = 3000;

commands = multiprocessing.Queue();
commits = multiprocessing.Queue();

hashmap = {};

class RepositoryError(Exception):
    pass

def create(key, data):
    if key not in hashmap:
        hashmap[key] = data;
    else:
        raise RepositoryError('Key already in use');

def read(key):
    try: 
        return hashmap[key];
    except KeyError:
        raise RepositoryError('Theres no data associated to this key');

def update(key, data):
    if(key in hashmap):
        hashmap[key] = data;
    else:
        raise RepositoryError('Theres no data associated to this key');

def delete(key):
    try: 
        del(hashmap[key]);
    except KeyError:
        raise RepositoryError('Theres no data associated to this key');

def log_add(commit):
    log = open('log', 'a');
    if commit.operation == 'CREATE' or commit.operation == 'UPDATE':
        s = commit.operation + str(commit.key) + '"' + commit.data + '"' + '\n';
    else:
        s = commit.operation + str(commit.key) + '\n';
    log.write(s);
    log.close();

def log_reexecute():
    log = open('log','r');
    for s in log:
        commit = commit_factory(s);
        process(commit);

def config_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    host = socket.gethostname();
    port = read_port();
    s.bind((host,port));
    return s

def read_port():
    config_file = open('server_config','r');
    port = int(config_file.read().split(':')[1]);
    config_file.close;
    return port;

class Commit(object):
    def __init__(self, operation, key, data):
        self.operation = operation;
        self.key = key;
        self.data = data;

def commit_factory(s):

    operation = None;
    key = None;
    data = None;

    #Extrai e valida "OPERATION"
    if s.replace(' ', '').find('CREATE') == 0:
        operation = 'CREATE';
    elif s.replace(' ', '').find('READ') == 0:
        operation = 'READ';
    elif s.replace(' ', '').find('UPDATE') == 0:
        operation = 'UPDATE';
    elif s.replace(' ', '').find('DELETE') == 0:
        operation = 'DELETE';
    else:
        raise ValueError('Invalid operation');

    #Extrai e valida "KEY"
    data_tuple = s.split(operation, 1)[1];
    if (operation == 'CREATE' or operation == 'UPDATE'):
        if data_tuple.find('"') < 0 or data_tuple.replace('"', '', 1).find('"') < 0:
            raise ValueError('Invalid key or data format');
        key = data_tuple.split('"', 1)[0];
    else:
        key = data_tuple;
    if not key:
        raise ValueError('Invalid key or data format');
    try: 
        key = int(key);
    except ValueError:
        raise ValueError('Invalid key or data format');
    if getsizeof(key) > KEY_MAX_SIZE:
        raise ValueError('Key size is too large');

    #Extrai e valida "DATA"
    if (operation == 'CREATE' or operation == 'UPDATE'):
        data_begin = data_tuple.find('"') + 1;
        data_end = data_tuple.rfind('"');
        data = data_tuple[data_begin:data_end];
        if not data:
            raise ValueError('Data cant be empty');
        if getsizeof(data) > DATA_MAX_SIZE:
            raise ValueError('Data size is too large');

    #Gera e retorna objeto do tipo Commit
    return Commit(operation, key, data);

def process_commands(server):
    while True:
        if (commands.qsize() > 0):
            command = commands.get();
            try:
                commit = commit_factory(command[0]);
                log_add(commit);
                commits.put((commit, command[1]));
            except ValueError as e:
                response = str(e);
                server.sendto(response.encode(), command[1]);

def process_commits(server):
    while (True):
        if(commits.qsize() > 0):
            commit = commits.get();
            response = process(commit[0]);
            server.sendto(response.encode(), commit[1]);

def process(commit):

    response = 'Command successfully executed'

    if commit.operation == 'CREATE':
        try:
            create(commit.key, commit.data);
        except RepositoryError as e:
            response = str(e);

    elif commit.operation == 'READ':
        try:
            return read(commit.key);
        except RepositoryError as e:
            response = str(e);

    elif commit.operation == 'UPDATE':
        try:
            update(commit.key, commit.data);
        except RepositoryError as e:
            response = str(e);

    elif commit.operation == 'DELETE':
        try:
            delete(commit.key);
        except RepositoryError as e:
            response = str(e);

    else:
        raise Exception('Invalid commit object found during execution');

    return response;

def main():

    server = config_server();
    log_reexecute();

    _thread.start_new_thread(process_commands, (server,));
    _thread.start_new_thread(process_commits, (server,));

    while(True):
        value, addr = server.recvfrom(read_port());
        commands.put((value.decode(), addr));
        print('Command received from', addr);

main();
