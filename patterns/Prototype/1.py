from abc import  ABC,abstractmethod
from copy import deepcopy

class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        ...

class Connection:
    def __init__(self,host,port,login,password):
        self.is_open = False
        self.host = host
        self.port = port
        self.login = login
        self.password = password

    def open(self):
        self.is_open = True
        print('Connection opened')

class Config:
    def __init__(self,topic,partition,offset):
        self.topic = topic
        self.partition = partition
        self.offset = offset

class Consumer(Cloneable):
    def __init__(self,connection:Connection,config:Config):
        self.connection = connection
        self.config = config

    def clone(self):
        return Consumer(self.connection,deepcopy(self.config))

    def start(self):
        if not self.connection.is_open:
            self.connection.open()
        print('start')


con1 = Connection('loc','1234','sysdba','not_mas')
conf = Config('top a','31',3111)
cons = Consumer(con1,conf)
cons.start()

cons2 = cons.clone()
cons2.config.offset = 77
cons.start()


