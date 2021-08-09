from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap

current_app = Flask(__name__)
current_app.config.from_object(Config)

bootstrap = Bootstrap(current_app)


from app import routes
