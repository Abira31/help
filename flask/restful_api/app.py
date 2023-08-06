from flask import Flask,request
from flask_restful import Resource,Api
from flask_jwt import JWT,jwt_required

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from securite import *

jwt = JWT(app, authenticate, identity)
items = []


class Item(Resource):

    def get(self,name):
        item = next(filter(lambda x:x['name'] == name,items),None)
        return {'item':None}, 404

    def post(self,name):
        if next(filter(lambda x:x['name'] == name,items),None) is not None:
            return {'message':"An item name '{}' ".format(name)}, 400
        data = request.get_json()
        item = {'name':name,'price':data['price']}
        items.append(item)
        return item,201

class ItemList(Resource):
    def get(self):
        return {'items':items}


api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
app.run(debug=True)


# from flask import Flask
# from flask_jwt import JWT, jwt_required, current_identity
#
# from flask_bcrypt import Bcrypt
#
# class User(object):
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.password = password
#
#     def __str__(self):
#         return "User(id='%s')" % self.id
#
# users = [
#     User(1, 'user1', 'abcxyz'),
#     User(2, 'user2', 'abcxyz'),
# ]
#
# username_table = {u.username: u for u in users}
# userid_table = {u.id: u for u in users}
#
# def authenticate(username, password):
#     user = username_table.get(username, None)
#     if user and bcrypt.check_password_hash(user.password.encode('utf-8'), password.encode('utf-8')):
#         return user
#
# def identity(payload):
#     user_id = payload['identity']
#     return userid_table.get(user_id, None)
#
# app = Flask(__name__)
# app.debug = True
# app.config['SECRET_KEY'] = 'super-secret'
# bcrypt = Bcrypt(app)
#
#
#
# jwt = JWT(app, authenticate, identity)
#
# @app.route('/protected')
# @jwt_required()
# def protected():
#     return '%s' % current_identity
#
# if __name__ == '__main__':
#     app.run()