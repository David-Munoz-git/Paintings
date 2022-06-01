from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.painting import Painting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def user():
    return render_template("loginRegg.html")


#=========================
#Register route
#=========================

@app.route("/register", methods=['POST'])
def register_user():
#1 validate form info
    if not User.validate_register(request.form):
        return redirect("/")
# 2- convert password via bcrypt
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
#2.5 collect data from form
    query_data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
#3 run query to database (INSERT)
    new_user_id = User.create_user(query_data)
    session['user_id'] = new_user_id
#4 redirect
    return redirect("/dashboard")

#=========================
#Login route
#=========================

@app.route("/login", methods=['POST'])
def login():
#1 - validate info
    if not User.validate_login(request.form):
        return redirect("/")

#2  - query based on data
    query_data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    logged_in_user = User.get_by_email(query_data)
    
#3 - put user_id into session
    session["user_id"] = logged_in_user.id
    return redirect("/dashboard")

#=========================
#Dashboard
#=========================


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You need to log in or register before you enjoy this site")
        return redirect("/")

    data = {
        "user_id": session['user_id']
    }

    user = User.get_user(data)

    all_paintings = Painting.get_all()

    return render_template("dashboard.html", user=user, all_paintings=all_paintings)


# =========================
# Logout
# =========================

@app.route("/logout")
def logout():
    session.clear()
    flash("you logged out!")
    return redirect("/")