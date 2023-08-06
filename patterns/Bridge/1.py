from abc import ABC,abstractmethod

class Driver(ABC):
    @abstractmethod
    def connect(self):
        ...
    @abstractmethod
    def disconnect(self):
        ...
    @abstractmethod
    def push(self,message):
        ...


class KafkaDriver(Driver):
    def connect(self):
        self._connect_to_broker()
    def _connect_to_broker(self):
        print('Connect to kafka broker')
    def _select_topic(self):
        print('Select topic')
    def disconnect(self):
        self._disconnect_from_broker()
    def _disconnect_from_broker(self):
        print('Disconnect from Kafka broker')
    def push(self,message):
        self._select_topic()
        print(f'Push message {message} into Kafka Topic')

class RedisDriver(Driver):
    def connect(self):
        self._connect_to_db()
    def _connect_to_db(self):
        print('Connect to Redis DB')
    def disconnect(self):
        self._disconnect_from_db()
    def _disconnect_from_db(self):
        print('Disconnect from Redis')
    def push(self,message):
        print(f'lpush message {message} into Redis queue')

class Producer(ABC):
    def __init__(self,driver:Driver):
        self.driver = driver
    @abstractmethod
    def send(self,message):
        ...

class MessageProducer(Producer):
    def send(self,message):
        self.driver.connect()
        self.driver.push(message)
        self.driver.disconnect()

class SecureMessageProducer(Producer):
    def send(self,message):
        encrupted_message = self._encrypt(message)
        self.driver.connect()
        self.driver.push(encrupted_message)
        self.driver.disconnect()
    def _encrypt(self,message):
        print('Encrypt message')
        return f'#_super_secure_{message}_#'


mes_pro = MessageProducer(RedisDriver())
mes_pro.send('12edw123ed')
print(10*'-')
ser_pro = SecureMessageProducer(KafkaDriver())
ser_pro.send('cvgretfg')

