class Car:
    def __init__(self,driver:'Driver'):
        self.driver = driver

    def drive(self):
        print(f'Car is being driven')


class Driver:
    def __init__(self,name,age):
        self.name = name
        self.age = age


class CarProxy:
    def __init__(self,driver:'Driver'):
        self.driver = driver
        self._car = Car(driver)

    def drive(self):
        if self.driver.age >= 16:
            self._car.drive()
        else:
            print('Drive too young')
            
driver = Driver('John',12)
car = CarProxy(driver)
car.drive()
