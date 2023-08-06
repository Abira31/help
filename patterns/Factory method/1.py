from abc import ABC,abstractmethod
import random
from enum import Enum

class User(ABC):
    ...

class MtsUser(User):
    def __init__(self,phone):
        print(f'Create MtsUser {phone}')

class LiteBoxUser(User):
    def __init__(self,email):
        print(f'Create LiteboxUser {email}')

class Credentials(ABC):
    ...

class MtsCredentials(Credentials):
    def __init__(self,phone,password):
        self._phone = phone
        self._password = password

    @property
    def phone(self):
        return self._phone

    @property
    def password(self):
        return self._password

class LiteboxCredentials(Credentials):
    def __init__(self,email,password):
        self._email = email
        self._password = password

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password


class Authenticator(ABC):
    @abstractmethod
    def authenticate(self,credentials:Credentials):
        ...

class LiteboxAuthenticator(Authenticator):
    def authenticate(self,credentials:LiteboxCredentials):
        print(credentials.email)
        return LiteBoxUser(credentials.email)


class MtsAuthenticator(Authenticator):
    def authenticate(self,credentials:MtsCredentials):
        print(credentials.phone)
        return MtsUser(credentials.phone)

def authenticate(authenticator:Authenticator,credentials:Credentials):
    return authenticator().authenticate(credentials)

phone = '123321'
password = '1232eq'

cred = MtsCredentials(phone,password)
user:MtsUser = authenticate(MtsAuthenticator,cred)


print(user)