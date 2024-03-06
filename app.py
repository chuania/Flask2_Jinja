from flask import Flask, request, render_template, abort, jsonify
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
BASE_DIR = Path(__file__).parent

app.config["JSON_AS_ASCII"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR / 'users.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    birth_date = db.Column(db.String(32))
    phone_number = db.Column(db.String(32), nullable=False)

    def __init__(self, login, last_name, name, surname, birth_date, phone_number):
        self.login = login
        self.last_name = last_name
        self.name = name
        self.surname = surname
        self.birth_date = birth_date
        self.phone_number = phone_number

    def __repr__(self):
        return f"User({self.login})"

    def to_dict(self):
        return {
            "id": self.id,
            "login": self.login,
            "last_name": self.last_name,
            "name": self.name,
            "surname": self.surname,
            "birth_date": self.birth_date,
            "phone_number": self.phone_number,
        }


@app.get("/")
def home():

    return render_template("index.html")


@app.get("/names")
def names():
    users = UserModel.query.all()
    entities = list()
    for user in users:
        entities.append(user.name)
    return render_template("names.html", entities=entities)


@app.get("/table")
def humans():
    users = UserModel.query.all()
    entities = list()
    for user in users:
        keys = ["last_name", "name", "surname"]
        values = [user.last_name, user.name, user.surname]
        item = dict(zip(keys, values))
        entities.append(item)
    return render_template("table.html", entities=entities)


@app.route("/users")
def users_list():
    users = UserModel.query.all()
    entities = list()
    for user in users:
        entities.append(user)
    return render_template("users_list.html", entities=entities)


@app.route("/users/<login>")
def get_user_by_login(login):
    users = UserModel.query.all()
    for user in users:
        if user.login == login:
            return render_template("user_info.html", item=user)
    else:
        abort(404, f"User with login = {login} not found")


@app.route("/about")
def about():
    return "О нас"


if __name__ == "__main__":
    app.run(debug=True)
