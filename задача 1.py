from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# Список пользователей (лучше хранить в базе данных)
users = {
    "username1": "password1",
    "username2": "password2"
}

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

    users[username] = password

    return render_template('profile.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run()
