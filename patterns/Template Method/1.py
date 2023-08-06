from abc import ABC,abstractmethod

class Scales(ABC):
    def get_weigth(self):
        self.before_connect()
        self.connect()
        self.after_connect()
        raw_data = self.read_raw_data()
        weigth = self.process_raw_data(raw_data)
        self.before_connect()
        self.disconnect()
        self.after_disconnect()
        return weigth
    def before_connect(self):
        ...
    @abstractmethod
    def connect(self):
        ...
    def after_connect(self):
        ...
    @abstractmethod
    def read_raw_data(self):
        ...
    def process_raw_data(self,data):
        return data
    def before_connect(self):
        ...
    @abstractmethod
    def disconnect(self):
        ...
    def after_disconnect(self):
        ...

class ScalesModelA(Scales):
    def connect(self):
        print('ScalesModelA are connecting through COM')
    def disconnect(self):
        print('ScalesModelA are disconnecting')
    def before_connect(self):
        print('ScalesModelA are preraring to connect')
    def read_raw_data(self):
        return 100

class ScalesModelX(Scales):
    def connect(self):
        print('ScalesModelX are connecting through Ethernet')

    def disconnect(self):
        print('ScalesModelX are disconnecting')

    def before_connect(self):
        print('ScalesModelX are preraring to connect')

    def read_raw_data(self):
        return 100

    def process_raw_data(self,data):
        return 0.001 * data

    def after_disconnect(self):
        print('ScalesModelX are shutting down port')


scales_model_a = ScalesModelA()
weight = scales_model_a.get_weigth()
print(weight)

scales_model_x = ScalesModelX()
weight = scales_model_x.get_weigth()
print(weight)
