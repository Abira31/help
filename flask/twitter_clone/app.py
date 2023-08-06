import os


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import ALL,UploadSet,configure_uploads





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{os.getcwd()}/twitter_clone.db'
app.config['SECRET_KEY'] = 'sdfgrewgedtk34otij34t'
app.config["UPLOADED_PHOTOS_DEST"] = "static/uploads/photos"

photos = UploadSet("photos", ALL)
configure_uploads(app, photos)


login_manager = LoginManager(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app,db)



@app.template_filter('time_since')
def time_since(delta):
    seconds = delta.total_seconds()
    days,seconds = divmod(seconds, 86400)
    hours,seconds = divmod(seconds, 3600)
    minutes,seconds = divmod(seconds, 60)

    if days > 0:
        return '%dd' % (days)
    elif hours > 0:
        return '%dh' % (hours)
    elif minutes > 0:
        return '%dm' % (minutes)
    else:
        return 'Just now'

from views import *

if __name__ == '__main__':
    app.run(debug=True)

