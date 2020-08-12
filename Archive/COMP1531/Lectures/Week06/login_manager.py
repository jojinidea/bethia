#we need a login mnager

from flask_login import LoginManager
from app import 

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(name):
    return user_manager.get_user(name)
