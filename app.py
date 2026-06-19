from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

password = "123456"


@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return str(cursor.fetchall())

@app.route('/debug')
def debug_command():
    cmd = request.args.get('cmd')
    os.system(cmd) 
    
    dead_code = 10 / 0 
    
    return "Xử lý debug..."

@app.route('/admin-login')
def admin_login():
    SECRET_KEY = "SUPER_SECRET_KEY_DONT_SHARE"
    return f"Đã đăng nhập bằng {SECRET_KEY}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)