from flask import Flask, redirect, render_template, request, url_for, flash, abort, session, g
import os
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import pymysql
import pymysql.cursors
import datetime

# конфигурация
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
key = "admin"  # Конец логина для панели главного администратора

app = Flask(__name__)
app.config.from_object(__name__)

# login_manager = LoginManager(app)


connection = pymysql.connect(host='khaliloy.beget.tech',
                             user='khaliloy_taxi',
                             password='123q123Q',
                             database='khaliloy_taxi',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def add_service(name, age, phone, date, time, address):
    db = pymysql.connect(host='khaliloy.beget.tech', user='khaliloy_taxi', passwd='123q123Q',
                         db='khaliloy_taxi', charset='utf8')
    cur = db.cursor()
    try:
        if address:
            sql = f"INSERT INTO us (`id`, `name`, `age`, `phone`, `date`, `time`, `address`, `status`) " \
              f"VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (name, age, phone, date, time, address, 0))
        else:
            sql = f"INSERT INTO tax (`id`, `name`, `age`, `phone`, `date`, `time`, `status`) " \
              f"VALUES (NULL, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (name, age, phone, date, time, 0))
        db.commit()
    except sqlite3.Error as e:
        print("Ошибка добавления информации в БД: " + str(e))
        return False
    return True


def get_service(type):
    try:
        db = pymysql.connect(host='khaliloy.beget.tech', user='khaliloy_taxi', passwd='123q123Q',
                             db='khaliloy_taxi', charset='utf8')
        cur = db.cursor()
        with db:
            cur.execute(f"SELECT * FROM {type} WHERE status = 1 ORDER BY id DESC")
            result = cur.fetchall()
            if result:
                return result
    except sqlite3.Error as e:
        print("Ошибка добавления информации в БД: " + str(e))
    return []


def get_all(type):
    try:
        db = pymysql.connect(host='khaliloy.beget.tech', user='khaliloy_taxi', passwd='123q123Q',
                             db='khaliloy_taxi', charset='utf8')
        cur = db.cursor()
        with db:
            cur.execute(f"SELECT * FROM {type} WHERE status = 0 ORDER BY id DESC")
            result = cur.fetchall()
            if result:
                return result
    except sqlite3.Error as e:
        print("Ошибка добавления информации в БД: " + str(e))
    return []


def change_st(type, id):
    try:
        db = pymysql.connect(host='khaliloy.beget.tech', user='khaliloy_taxi', passwd='123q123Q',
                             db='khaliloy_taxi', charset='utf8')
        cur = db.cursor()
        cur.execute(f"UPDATE {type} SET status = 1 WHERE id = {id} LIMIT 1")
        db.commit()
    except sqlite3.Error as e:
        print("Ошибка изменения статуса объявления на 1 в БД: " + str(e))
    return True


@app.route("/", methods=["POST", "GET"])
# @login_required
def main():
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    return render_template("main.html")


@app.route("/driver", methods=["POST", "GET"])
# @login_required
def driver():
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    return render_template("driver.html")


@app.route("/driver/add", methods=["POST", "GET"])
# @login_required
def driver_add():
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    if request.method == 'POST':
        res = add_service(request.form['name'], request.form['age'], request.form['phone'], request.form['date'], request.form['time'], address=None)
        if not res:
            flash('Ошибка добавления сообщения', category='error')
            print("Ошибка добавления сообщения")
            return redirect(url_for('driver_add'))
        else:
            flash('Сообщение добавлено успешно', category='success')
            print("Сообщение добавлено успешно")
            return redirect(url_for('driver_add'))
    return render_template("driver_add.html")


@app.route("/driver/see", methods=["POST", "GET"])
# @login_required
def driver_see():
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    return render_template("driver_see.html", req=get_service("us"))


@app.route("/client", methods=["POST", "GET"])
# @login_required
def client():
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    return render_template("client.html")


@app.route("/client/add", methods=["POST", "GET"])
# @login_required
def client_add():
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    if request.method == 'POST':
        res = add_service(request.form['name'], request.form['age'], request.form['phone'], request.form['date'], request.form['time'], request.form['address'])
        if not res:
            flash('Ошибка добавления сообщения', category='error')
            print("Ошибка добавления сообщения")
            return redirect(url_for('client_add'))
        else:
            flash('Сообщение добавлено успешно', category='success')
            print("Сообщение добавлено успешно")
            return redirect(url_for('client_add'))
    return render_template("client_add.html")


@app.route("/client/see", methods=["POST", "GET"])
# @login_required
def client_see():
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    return render_template("client_see.html", req=get_service("tax"))


@app.route("/moder", methods=["POST", "GET"])
# @login_required
def moder():
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    if request.method == 'POST':
        if request.form['login'] == "log" and request.form['psw'] == "123":
            print("Ошибка добавления сообщения")
            return redirect(url_for('edit'))
        else:
            flash('Ошибка авторизации', category='error')
            return redirect(url_for('moder'))
    return render_template("moder.html")


@app.route("/edit", methods=["POST", "GET"])
# @login_required
def edit():
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    return render_template("edit.html")


@app.route("/edit_client", methods=["POST", "GET"])
# @login_required
def edit_client():
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    return render_template("edit_client.html", req=get_all("us"))


@app.route("/edit_driver", methods=["POST", "GET"])
# @login_required
def edit_driver():
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    return render_template("edit_driver.html", req=get_all("tax"))


@app.route("/edit_driver/<id>", methods=["POST", "GET"])
# @login_required
def edit_driver_st(id):
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    change_st("tax", id)
    return redirect(url_for("edit_driver"))


@app.route("/edit_client/<id>", methods=["POST", "GET"])
# @login_required
def edit_client_st(id):
    # login = session['userLogged']
    # user_name, user_description, datetime = dbase.get_user_info(login)
    change_st("us", id)
    return redirect(url_for("edit_client"))


@app.errorhandler(404)
def page_not_found(error):
    print("Ошибка 404")
    return render_template('page404.html', title="Страница не найдена"), 404


@app.errorhandler(401)
def not_authorized(error):
    print("Ошибка 401")
    return render_template('page401.html', title="Не авторизован"), 401


if __name__ == "__main__":
    app.run(debug=True)
