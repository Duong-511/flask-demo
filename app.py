from flask import Flask, request
import sqlite3

app = Flask(__name__)

password = "123456"

@app.route('/user')
def get_user():

    user_id = request.args.get('id')

    conn = sqlite3.connect('test.db')

    query = "SELECT * FROM users WHERE id = " + user_id

    result = conn.execute(query)

    return str(result.fetchall())

app.run(host='0.0.0.0', port=5000)