from flask import Flask
app = Flask(__name__)
app.config.from_object('portfolio1.config')

from .main import User

import portfolio1.main