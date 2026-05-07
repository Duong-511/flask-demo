from flask import Flask, request
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
csrf = CSRFProtect(app)

password = "123456"

