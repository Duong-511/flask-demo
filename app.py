from flask import Flask, request
from flask_wtf.csrf import CSRFProtect
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
csrf = CSRFProtect(app)

password = os.getenv("password") # Compliant

