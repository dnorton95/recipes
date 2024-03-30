from flask_app import app
from flask_app.models.recipe import Recipe_class
from flask_app.models.user import User_class
from flask import flash, render_template, redirect, request, session


@app.route("/recipes/all")
def recipes():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    recipes = Recipe_class.find_all_recipes_with_users()
    user = User_class.find_user_by_id(session["user_id"])
    return render_template("all_recipes.html", recipes=recipes, user=user)


@app.get("/recipes/new")
def new_recipe():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    user = User_class.find_user_by_id(session["user_id"])
    flash("Recipe succesfully posted")
    return render_template("new_recipe.html", user=user)

@app.post("/recipes/create")
def create_recipe():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    if not Recipe_class.recipe_is_valid(request.form):
        return redirect("/recipes/new")
    recipe_input_data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date_cooked"],
        "thirty_min": request.form["thirty_min"],
        "user_id": request.form["user_id"],


    }
    recipe_id = Recipe_class.new_recipe(recipe_input_data)
    return redirect("/recipes/all")

@app.get("/recipes/<int:recipe_id>")
def recipe_details(recipe_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    recipe = Recipe_class.find_recipe_by_id_with_user(recipe_id)
    formatted_date = recipe.date_cooked.strftime("%m/%d/%Y")
    recipe.date_cooked = formatted_date
    user = User_class.find_user_by_id(session["user_id"])
    return render_template("recipe_details.html", user=user, recipe=recipe, formatted_date=formatted_date)

@app.get("/recipes/<int:recipe_id>/edit")
def edit_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    recipe = Recipe_class.find_recipe_by_id(recipe_id)
    user = User_class.find_user_by_id(session["user_id"])
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
    if not Recipe_class.recipe_is_valid(request.form):
        flash("Invalid recipe data.", "error")
        return redirect(f"/recipes/{recipe_id}/edit")
    
    # Update the recipe using Recipe_class.update() method
    Recipe_class.update(recipe_id, request.form)

    flash("Recipe successfully updated")
    return redirect(f"/recipes/{recipe_id}")

@app.post("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    Recipe_class.delete_by_id(recipe_id)
    return redirect("/recipes/all")
