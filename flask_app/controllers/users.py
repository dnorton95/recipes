# This will be in your controllers folder.  Remember to 'pipenv install flask pymysql flask_bcrypt' in your main project folder!
from flask_app import app, bcrypt
from flask import flash, render_template, redirect, request, session
from flask_app.models.user import User

# Replace all "Users/user" with your class name!


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/users/register")
def register():
    if not User.validate_register(request.form):
        return redirect("/")

    potential_user = User.find_by_email(request.form["email"])

    if potential_user != None:
        flash("Email in user!  Please log in!", "register")
        return redirect("/")

    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    user_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw,
    }
    user_id = User.create(user_data)
    session["user_id"] = user_id
    return redirect("/users/dashboard")


@app.get("/users/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You must be logged in to view that page.", "login")
        return redirect("/")
    user = User.find_by_id({session["user_id"]})
    return render_template("dashboard.html", user=user)


@app.post("/users/login")
def login():
    if not User.validate_login(request.form):
        return redirect("/")
    potential_user = User.find_by_email(request.form["email"])
    if potential_user == None:
        flash("Invalid credentials", "login")
        return redirect("/")

    user = potential_user

    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials", "login")
        return redirect("/")

    session["user_id"] = user.id
    return redirect("/users/dashboard")


@app.route("/users/logout")
def logout():
    session.clear()
    return redirect("/")
