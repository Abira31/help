import uuid
from uuid import UUID

class UserSignup:
    def __init__(self,login,password):
        self.login = login
        self.password = password

class C1:
    def make_invoice(self,user_id:str,license_price:int):
        print(f'1C: Выставление счета клиенту с id {user_id} на сумму {license_price} рублей')

class AuthServer:
    def signup(self,user_signup:UserSignup):
        print(f'CA: Регистрируем пользователя с логином {user_signup.login}')
        return uuid.uuid4()

class NodeServer:
    def create_layer(self):
        print('CH:Иннициализируем данные для нового слоя')
        return uuid.uuid4()

    def link_user_to_layer(self,user_id:str,layer_id:str):
        print(f'CH: Связываем пользователя с id {user_id} со слоем {layer_id}')


class Promo:
    discount = 500

    def verify_promocode(self,promocode:str):
        print(f'Промо: Выполняем проверку промокода {promocode}')
        return self.discount if promocode.startswith('VALID') else 0

class Billing:
    license_price = 2000

    def get_license_price(self,discount: int):
        return self.license_price - discount


class RegistrationFacade:
    def __init__(self):
        self.c1 = C1()
        self.auth_server = AuthServer()
        self.node_server = NodeServer()
        self.promo = Promo()
        self.billing = Billing()

    def signup(self,user_signup:UserSignup,promocode=None):
        user_id = self.auth_server.signup(user_signup)
        layer_id = self.node_server.create_layer()
        self.node_server.link_user_to_layer(user_id,layer_id)
        discount = 0
        if promocode:
            discount = self.promo.verify_promocode(promocode)
        license_prise = self.billing.get_license_price(discount)
        self.c1.make_invoice(user_id,license_prise)

user_signup = UserSignup('123wqe213','dsadewqe213')
registration_facade = RegistrationFacade()
registration_facade.signup(user_signup,'VALID_PROMO_1')


