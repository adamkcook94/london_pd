import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/pending_inv")
def pending_inv():
    pending = mongo.db.pending.find()
    return render_template("pending.html", pending=pending)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)


# if request.method == "POST":
#         existing_user = mongo.db.users.find_one(
#             {"username": request.form.get("username").lower()
#              })
#         if existing_user:
#             if check_password_hash(
#                     existing_user["password"], request.form.get("password")):
#                 session["admin"] = request.form.get("username").lower()
#             flash("Welcome {}".format(request.form.get("username")))
#         else:
#             flash("Incorrect Username or Password")
#             return redirect(url_for("admin_login"))
#     else:
#         flash("Incorrect Username or Password")
#         return redirect(url_for("admin_login"))
