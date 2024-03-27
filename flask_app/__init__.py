# __init__.py will look like this most of the time!
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "Secret secret tunnel"
# Remember, this goes INSIDE the flask_app folder!  Only server.py and the Pipfiles live in the main project directory!