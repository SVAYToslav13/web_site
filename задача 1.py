from flask import Flask, request, render_template, redirect
#from flask_sqlalchemy import SQLAlchemy
import csv
import subprocess

perm = False
suc = False
app = Flask(__name__)
# Список пользователей (лучше хранить в базе данных)
users = []

csv_file_path = 'C:/Users/Лев/PycharmProjects/pythonProject/templates/users.csv'
def check_task(trak):
    # Чтение кода из файла
    with open(trak, 'r') as file:
        code = file.read()
    print(code)
    # Тесты, которые ожидаем для выполнения
    test_cases = ['hi', 'r']

    for test_case in test_cases:
        # Выполнение кода и получение его вывода
        process = subprocess.Popen(['python', '-c', code], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        output, _ = process.communicate(test_case.encode())

        # Проверка вывода на правильность
        expected_output = 'hi'
        print(output.decode().strip())
        if output.decode().strip() == expected_output:
            print(f"Test case {test_case} passed")
            return True
        else:
            print(f"Test case {test_case} failed")
            return False

def check_task_1(trak):
    # Чтение кода из файла
    with open(trak, 'r') as file:
        code = file.read()
    print(code)
    # Тесты, которые ожидаем для выполнения
    age = int(input("Введите ваш возраст: "))
    if age >= 18:
        if "Совершеннолетний" in str():
            print("Верно")
        else:
            print("Неверно")
    else:
        if "Несовершеннолетний" in str():
            print("Верно")
        else:
            print("Неверно")
def check_login_and_password(login, password):
    with open(csv_file_path, mode='r', newline='', encoding="utf8") as file:
        read = csv.reader(file)
        n = login not in list(read)
        if login.isalnum() and password.isalnum() and n:
            return True
        else:
            return False


def write_in_csv(user):
    with open(csv_file_path, mode='w', newline='\n', encoding="utf8") as file:
        writer = csv.writer(file, delimiter=",", lineterminator="\r")
        writer.writerow(user)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    global perm
    if perm:
        return render_template('entrance.html')
    else:
        return render_template('unsucces.html')

@app.route('/login1', methods=['POST'])
def login1():
    global perm
    global suc
    if perm:
        username = request.form['username']
        password = request.form['password']

        if check_login_and_password(username, password):
            suc = True
            return render_template('success.html')
        else:
            return "Неверное имя пользователя или пароль"
    else:
        return render_template('unsucces.html')

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/register1', methods=['POST'])
def register1():
    global perm
    username = request.form['username']
    password = request.form['password']

    if username == None or password == None:
        return render_template('error.html')

    elif check_login_and_password(username, password):
        users.append(username)
        users.append(password)
        write_in_csv(users)
        perm = True
        return render_template('reg.html')
    else:
        return render_template('error.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/task')
def task():
    global suc
    global perm
    if perm and suc:
        return render_template('task.html')
    else:
        return render_template('unreg.html')

@app.route('/task1' , methods=['POST'])
def task1():
    file = request.form['text']
    if check_task(file):
        return render_template('true.html')
    else:
        return render_template('error.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admins')
def admins():
    return render_template('admins.html')

if __name__ == '__main__':
    app.run(debug=True)
