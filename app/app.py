import os
from flask import Flask
from flask_wtf import CSRFProtect
import secrets

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
app=Flask(__name__, 
          template_folder=os.path.join(ROOT_DIR, "templates"), 
          static_folder=os.path.join(ROOT_DIR, "static")) 
app.secret_key = secrets.token_hex(16)
csrf = CSRFProtect(app)

import routes