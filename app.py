from flask import Flask, request
from flask_wtf.csrf import CSRFProtect
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
csrf = CSRFProtect(app)

password = os.getenv("password") # Compliant

@app.route('/user')
def get_user():

    user_id = request.args.get('id')

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE id = '{user_id}'"

    cursor.execute(query)

    return "done"

app.run(host='0.0.0.0', port=5000)