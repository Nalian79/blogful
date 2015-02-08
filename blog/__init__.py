import os

from flask import Flask
from database import session

# ask mentor why this has to come before the below imports.
app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")
app.config.from_object(config_path)

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

import views
import filters

import login
