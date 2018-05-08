import grpc

import redes3_pb2
import redes3_pb2_grpc
import _thread;
import sys


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = redes3_pb2_grpc.Redes3Stub(channel)
    while True:
        command = input('> ');
        if (command.find('LISTEN') == 0):
            try:
                key = int(command.split('LISTEN')[1]);
                _thread.start_new_thread(print_logs(stub, key));
            except ValueError:
                print('Invalid key format');
        else:
            stub.execute_command(redes3_pb2.Command(command=command));

def print_logs(stub, key):

    for log in stub.listen(redes3_pb2.ListenRequest(key=str(key))):
        sys.stdout.write('[KEY ' + str(key) + ' LISTENER] ' + log.log + "\n> ")

if __name__ == '__main__':
    run()
