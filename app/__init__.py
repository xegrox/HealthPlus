from flask import Flask
from app.blueprints import home

app = Flask(__name__)
app.static_folder = 'static/dist'
app.register_blueprint(home)
