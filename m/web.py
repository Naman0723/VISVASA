from flask import Flask, request, redirect, render_template, url_for,flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key=b'\xa3\x8ao\x13b]\x1f;{\xff\xd2\x9ei\x9b\xd7e\x96\xb6\xfdA\x11\r\xf5,'

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['user_database']
users = db['users']

@app.route('/')
def home():
    return render_template('./signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users.find_one({'username': username}):
            flash('Username already exists.')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        users.insert_one({'username': username, 'password': hashed_password})
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            return redirect(url_for('mainwebsite'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('./login.html')

@app.route('/index')
def mainwebsite():
    return render_template('./index.html')

if __name__ == '__main__':
    app.run(debug=True)
