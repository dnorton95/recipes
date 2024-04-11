from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.models.comment import Comment
from flask import flash, render_template, redirect, request, session


@app.route("/recipes/all")
def recipes():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    recipes = Recipe.find_all_recipes_with_users()
    user = User.find_user_by_id(session["user_id"])

    return render_template("all_recipes.html", recipes=recipes, user=user)

@app.get("/recipes/new")
def new_recipe():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    user = User.find_user_by_id(session["user_id"])
    return render_template("new_recipe.html", user=user)

@app.post("/recipes/create")
def create_recipe():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    if not Recipe.form_is_valid(request.form):
        return redirect("/recipes/new")

    if "comments" in request.form:
        session["comments"] = request.form["comments"]


    if Recipe.count_by_name(request.form["name"]) >= 1:
        session["comments"] = request.form["comments"]
        flash("Recipe already exists!")
        return redirect("/recipes/new")

    if "comments" in session:
        session.pop("comments")

    Recipe.create(request.form)
    flash("Recipe succesfully posted")
    return redirect("/recipes/all")

@app.get("/recipes/<int:recipe_id>")
def recipe_details(recipe_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    recipe_comments = Comment.all_comments(recipe_id)
    recipe = Recipe.find_recipe_by_id_with_user(recipe_id)
    user = User.find_user_by_id(session["user_id"])
    formatted_date = recipe.date_cooked.strftime("%m/%d/%Y")
    recipe.date_cooked = formatted_date
    return render_template("recipe_details.html", user=user, recipe=recipe, recipe_comments=recipe_comments, formatted_date=formatted_date)


@app.get("/recipes/<int:recipe_id>/edit")
def edit_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    recipe = Recipe.find_recipe_by_id(recipe_id)
    user = User.find_user_by_id(session["user_id"])
    return render_template("edit_recipe.html", recipe=recipe, user=user)

@app.post("/recipes/update")
def update_recipe():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    if "recipe_id" not in request.form:
        flash("Recipe ID is missing.", "error")
        return redirect("/")

    recipe_id = request.form["recipe_id"]

    # Validate the existence of recipe_id and other necessary form fields
    if not Recipe.form_is_valid(request.form):
        flash("Invalid recipe data.", "error")
        return redirect(f"/recipes/{recipe_id}/edit")
    
    # Update the recipe using Recipe.update() method
    Recipe.update(recipe_id, request.form)

    flash("Recipe successfully updated")
    return redirect(f"/recipes/{recipe_id}")

@app.post("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    Recipe.delete_by_id(recipe_id)
    return redirect("/recipes/all")
