from flask import Flask, request
import sqlite3

app = Flask(__name__)
password = "123456"

@app.route('/')
def index():
    
    db = sqlite3.connect('database.db')
    return "Hệ thống đang hoạt động!"

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000)