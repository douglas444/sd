import multiprocessing;
import socket;
import _thread;
import queue;
from data_base import Data_base;
from data_base import RepositoryError;
from commit import Commit;
from enum import Enum;
from sys import getsizeof;
from concurrent import futures;
import grpc;
import redes3_pb2;
import redes3_pb2_grpc;
from snapshoter import Snapshoter;
from snapshoter import SnapshoterState;


commands = multiprocessing.Queue();
commits = multiprocessing.Queue();

data_base = Data_base();

class Assyncronous_responses():
    Queues = [];
    def __init__(self):
        pass;

    @staticmethod
    def Create_Queue():
        Assyncronous_responses.Queues.append(multiprocessing.Queue());
        return len(Assyncronous_responses.Queues) - 1;

    @staticmethod
    def Get_Queue(indice):
        try:
            q = Assyncronous_responses.Queues[indice];
            return q
        except ValueError as e:
            print("there is not a queue with that indice");
            return e;

class Listen_Udp():
    upd_log = [];
    chaves_observadas = {};

    @staticmethod
    def addClientListen(id,cliente):
        if id not in Listen_Udp.chaves_observadas:
            Listen_Udp.chaves_observadas[id] = [cliente];
        elif client not in Listen_Udp.chaves_observadas[id]:
            Listen_Udp.chaves_observadas[id].append(cliente);

    @staticmethod
    def Send_updates(server):
        last_index = 0;
        while(True):
            while (len(Listen_Udp.upd_log) > last_index):
                c = Listen_Udp.upd_log[last_index];
                if c.key in Listen_Udp.chaves_observadas:
                    for cliente in Listen_Udp.chaves_observadas[c.key]:
                        if (c.data != None):
                            server.sendto(str(c.operation + ' ' + c.data).encode(), cliente);
                        else:
                            server.sendto(str(c.operation).encode(), cliente);
                last_index += 1;



class Redes3(redes3_pb2_grpc.Redes3Servicer):

    grpc_log = [];
    def execute_command(self, request, context):
        result_queue = Assyncronous_responses.Create_Queue();
        commands.put((request.command, None, result_queue));
        return redes3_pb2.Log(log= Assyncronous_responses.Get_Queue(result_queue).get(block=True));

    def listen(self, request, context):
        last_index = len(self.grpc_log);
        while True:
            while len(self.grpc_log) > last_index:
                print(last_index)
                if self.grpc_log[last_index].key == int(request.key):
                    n = self.grpc_log[last_index]
                    if (n.data != None):
                        yield redes3_pb2.Log(log=str(n.operation + ' ' + n.data))
                    else:
                        yield redes3_pb2.Log(log=str(n.operation))
                last_index += 1;



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
        process(commit,None);

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
        command = commands.get(block=True);
        try:
            commit = Commit(command[0]);
            log_add(commit);
            commits.put((commit, command[1], command[2]));
            Redes3.grpc_log.append(commit);
            Listen_Udp.upd_log.append(commit);

        except ValueError as e:
            response = str(e);
            if command[1] == None:
                print(response);
            else:
                server.sendto(response.encode(), command[1]);

def process_commits(server):
    while (True):
        commit = commits.get(block=True);
        response = process(commit[0],commit[1]);
        if commit[1] != None:
            server.sendto(response.encode(), commit[1]);
        if commit[2] != None:
            Assyncronous_responses.Get_Queue(commit[2]).put(response);
def process(commit,client_addr):

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

    elif commit.operation == 'LISTEN':
        if(client_addr != None):
            Listen_Udp.addClientListen(commit.key,client_addr);
    else:
        raise Exception('Invalid commit object found during execution');

    return response;

def main():

    server = config_server();

    snapshoter = Snapshoter(data_base);
    snapshoter.loadSnapshot();
    snap_state = snapshoter.getState();
    if(snap_state != SnapshoterState.DELETING_LOG):
        log_reexecute();
    _thread.start_new_thread(snapshoter.startSnapshoter,());

    _thread.start_new_thread(process_commands, (server,));
    _thread.start_new_thread(process_commits, (server,));
    _thread.start_new_thread(grpc_server, ());
    _thread.start_new_thread(Listen_Udp.Send_updates, (server,));

    while(True):
        value, addr = server.recvfrom(read_port());
        commands.put((value.decode(), addr, None));
        print('Command received from', addr);

main();
