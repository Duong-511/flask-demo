from flask import Flask, request
import sqlite3

app = Flask(__name__)

password = "123456"

@app.route('/')
def index():
    db = sqlite3.connect('database.db')
    
    return "Hệ thống đang hoạt động!"

@app.route('/user')
def get_user():
    user_id = request.args.get('id') # Người dùng nhập: 1 OR 1=1
    
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + user_id
    
    cursor.execute(query)
    return str(cursor.fetchall())

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)