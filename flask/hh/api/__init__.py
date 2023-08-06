from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
import config
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
api = Api(app,prefix='/api/v1')
jwt = JWTManager(app)



SWAGGER_URL = '/api/docs'
API_URL = '/static/docs/openapi/swagger.yml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL
)
app.register_blueprint(swaggerui_blueprint)


from . import routes




