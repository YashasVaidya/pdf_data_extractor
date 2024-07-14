from flask import Flask
from config import Config
import os
import sqlite3

app = Flask(__name__, 
            template_folder=os.path.abspath('templates'),
            static_folder=os.path.abspath('static'))
app.config.from_object(Config)

def init_db():
    with app.app_context():
        db = sqlite3.connect(app.config['DATABASE'])
        with open(os.path.join(app.root_path, '..', 'schema.sql'), 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("Database initialized successfully")

# Always initialize the database when the app starts
init_db()

from app import routes