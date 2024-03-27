from flask_app import app
form flask_app.models.gizmo import Gizmo
from flask_app.models.user import User
from flask import flash, render_template, redirect, request, session


@app.route("/gizmos/all")
def gizmos():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    gizmos = Gizmo.find_all_with_users()
    user = User.find_by_id(session["user_id"])
    return render_template("all_gizmos.html", gizmos=gizmos, user=user)

@app.get("/gizmos/new")
def new_gizmo():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    user = User.find_by_id(session["user_id"])
    return render_template("new_gizmo.html", user=user)

@app.post("/gizmos/create")
def create_gizmo():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    if not Gizmo.form_is_valid(request.form):
        return redirect("/gizmos/new")
    
    return redirect("/gizmos/all")

@app.get("/gizmos/<int:gizmo_id>")
def gizmo_details(gizmo_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    gizmo = Gizmo.find_by_id_with_user(gizmo_id)
    user = User.find_by_id(session["user_id"])
    return render_template("gizmo_details.html", user=user, gizmo=gizmo)

@app.get("/gizmos/<int:gizmo_id>/edit")
def edit_gizmo(gizmo_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    gizmo = Gizmo.find_by_id(gizmo_id)
    user = User.find_by_id(session["user_id"])
    return render_template("edit_gizmo.html", gizmo=gizmo, user=user)

@app.post("/gizmos/update")
def update_gizmo():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    gizmo_id = request.form["gizmo_id"]
    if not Gizmo.form_is_valid(request.form):
        return redirect(f"/gizmos/{gizmo_id}/edit")
    
    Gizmo.update(request.form)
    return redirect(f"/gizmos/{gizmo_id}")

@app.post("/gizmos/<int:gizmo_id>/delete")
def delete_gizmo(gizmo_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    Gizmo.delete_by_id(gizmo_id)
    return redirect("/gizmos/all")
