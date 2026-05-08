from flask import Flask, request
import sqlite3

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

password = os.getenv("password")

@app.route('/')
def index():
    
    db = sqlite3.connect('database.db')
    db.close()
    return "Hệ thống đang hoạt động!"

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000)