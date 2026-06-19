from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# [LỖI CŨ] Hardcoded password
password = "123456"

@app.route('/')
def index():
    db = sqlite3.connect('database.db')
    return "Hệ thống đang hoạt động!"

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # [LỖI CŨ] SQL Injection hoành tráng
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return str(cursor.fetchall())

# ========================================================
# CHÈN THÊM CÁC LỖI MỚI VÀO ĐÂY ĐỂ ĐẢM BẢO QUÉT LÀ FAILED
# ========================================================

@app.route('/debug')
def debug_command():
    # 1. LỖI BẢO MẬT NGHIÊM TRỌNG (Vulnerability - Critical): Command Injection
    # Chạy lệnh hệ thống trực tiếp từ dữ liệu người dùng nhập vào mà không kiểm tra.
    cmd = request.args.get('cmd')
    os.system(cmd) 
    
    # 2. LỖI BUG CHẮC CHẮN GÂY CHẾT APP (Bug - Blocker): Tự chia cho số 0
    # SonarQube sẽ bắt được ngay lỗi logic này là lỗi gây crash ứng dụng.
    dead_code = 10 / 0 
    
    return "Xử lý debug..."

@app.route('/admin-login')
def admin_login():
    # 3. THÊM LỖI BẢO MẬT MỚI: Hardcoded khóa bí mật khác công khai
    SECRET_KEY = "SUPER_SECRET_KEY_DONT_SHARE"
    return f"Đã đăng nhập bằng {SECRET_KEY}"

if __name__ == '__main__':
    # 4. BẬT DEBUG MODE (Security Hotspot / Vulnerability)
    # Việc chạy app công khai host '0.0.0.0' kết hợp debug=True là điều tối kỵ khi lên production.
    app.run(host='0.0.0.0', port=5000, debug=True)