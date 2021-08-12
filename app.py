from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    pr = db.relationship('Profiles', backref='users', uselist=False)


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


@app.route("/")
def index():
    info = []
    try:
        info = Users.query.all()
        # info = Users.query.filter(Users.id > 1).all()
    except:
        print("Ошибка чтения из БД")

    return render_template("index.html", title="Главная", list=info)


@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        try:
            db.create_all()
            u = Users(email=request.form['email'], psw=request.form['psw'])
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

        return redirect(url_for('index'))

    return render_template("register.html", title="Регистрация")


if __name__ == "__main__":
    app.run(debug=True)

