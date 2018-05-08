
class RepositoryError(Exception):
    pass

class Data_base():
    
    def __init__(self):
        self.hashmap = {};

    def create(self,key, data):
        if key not in self.hashmap:
            self.hashmap[key] = data;
        else:
            raise RepositoryError('Key already in use');

    def read(self,key):
        try: 
            return self.hashmap[key];
        except KeyError:
            raise RepositoryError('Theres no data associated to this key');

    def update(self,key, data):
        if(key in self.hashmap):
            self.hashmap[key] = data;
        else:
            raise RepositoryError('Theres no data associated to this key');

    def delete(self,key):
        try: 
            del(self.hashmap[key]);
        except KeyError:
            raise RepositoryError('Theres no data associated to this key');