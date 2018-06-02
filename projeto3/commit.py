from sys import getsizeof;

KEY_MAX_SIZE = 28;
DATA_MAX_SIZE = 3000;

class Commit(object):
    def __init__(self, s):
        (operation, key, data) = Commit.commit_factory(s);
        self.operation = operation;
        self.key = key;
        self.data = data;
    
    @staticmethod
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
        elif s.replace(' ','').find('LISTEN') == 0:
            operation = 'LISTEN';
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
        return (operation, key, data);