import multiprocessing;
import socket;
import _thread;
import queue;
from data_base import Data_base;
from data_base import RepositoryError;
from commit import Commit;
from enum import Enum;
from sys import getsizeof;
from concurrent import futures
import grpc
import redes3_pb2
import redes3_pb2_grpc

commands = multiprocessing.Queue();
commits = multiprocessing.Queue();

data_base = Data_base();

class Redes3(redes3_pb2_grpc.Redes3Servicer):

    grpc_log = [];

    def execute_command(self, request, context):
        commands.put((request.command, None))
        return redes3_pb2.Void();

    def listen(self, request, context):
        last_index = 0;
        while True:
            while len(self.grpc_log) > last_index:
                print(last_index)
                if self.grpc_log[last_index].key == int(request.key):
                    n = self.grpc_log[last_index]
                    if (n.data != None):
                        yield redes3_pb2.Log(log=str(n.operation + ' ' + n.data))
                    else:
                        yield redes3_pb2.Log(log=str(n.operation))
                last_index += 1
        
        

def grpc_server():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    redes3_pb2_grpc.add_Redes3Servicer_to_server(Redes3(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    while True:
        pass

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
        commit = Commit(s);
        process(commit);

def config_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    host = socket.gethostname();
    port = read_port();
    s.bind((host,port));
    return s

def read_port():
    config_file = open('server_config', 'r');
    port = int(config_file.read().split(':')[1]);
    config_file.close;
    return port;

def process_commands(server):
    while True:
        if commands.qsize() > 0:
            command = commands.get();
            try:
                commit = Commit(command[0]);
                log_add(commit);
                commits.put((commit, command[1]));
                Redes3.grpc_log.append(commit);
            except ValueError as e:
                response = str(e);
                if command[1] == None:
                    print(response);
                else:
                    server.sendto(response.encode(), command[1]);

def process_commits(server):
    while (True):
        if(commits.qsize() > 0):
            commit = commits.get();
            response = process(commit[0]);
            if commit[1] != None:
                server.sendto(response.encode(), commit[1]);

def process(commit):

    response = 'Command successfully executed'

    if commit.operation == 'CREATE':
        try:
            data_base.create(commit.key, commit.data);
        except RepositoryError as e:
            response = str(e);

    elif commit.operation == 'READ':
        try:
            return data_base.read(commit.key);
        except RepositoryError as e:
            response = str(e);

    elif commit.operation == 'UPDATE':
        try:
            data_base.update(commit.key, commit.data);
        except RepositoryError as e:
            response = str(e);

    elif commit.operation == 'DELETE':
        try:
            data_base.delete(commit.key);
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
    _thread.start_new_thread(grpc_server, ());

    while(True):
        value, addr = server.recvfrom(read_port());
        commands.put((value.decode(), addr));
        print('Command received from', addr);

main();
