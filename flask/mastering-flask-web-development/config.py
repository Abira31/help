from distutils.command.clean import clean
from distutils.log import debug


class Config():
    pass

class ProdConfing():
    pass

class DevConfig():
    debug = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"