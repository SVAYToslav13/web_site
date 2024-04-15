from flask import Flask, request, render_template, redirect


app = Flask(__name__)

# Список пользователей (лучше хранить в базе данных)
users = {}

def check_login_and_password(login, password):
    if login.isalnum() and password.isalnum():
        return True
    else:
        return False


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('entrance.html')

@app.route('/login1', methods=['POST'])
def login1():
    username = request.form['username']
    password = request.form['password']

    if users.get(username) != password:
        return "Неверное имя пользователя или пароль"
    else:
        return render_template('profile.html')

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/register1', methods=['POST'])
def register1():
    username = request.form['username']
    password = request.form['password']

    if check_login_and_password(username, password):
        users[username] = password
        return render_template('profile.html')
    else:
        return render_template('error.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/task')
def task():
    return render_template('task.html')

@app.route('/task1', methods=['POST'])
def task1():
    username = request.form['username']
    print(username)
    return render_template('true.html')

if __name__ == '__main__':
    app.run(debug=True)
