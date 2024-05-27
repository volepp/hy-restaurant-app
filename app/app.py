import os
from flask import Flask

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
app=Flask(__name__, 
          template_folder=os.path.join(ROOT_DIR, "templates"), 
          static_folder=os.path.join(ROOT_DIR, "static")) 

import routes