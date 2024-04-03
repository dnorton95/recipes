from flask_app import app
from flask_app.models.comment import Comment
from flask import flash, render_template, redirect, request, session


@app.post("/comments/create")
def create_comment():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    print("Before retrieving recipe_id from form")
    recipe_id = request.form.get("recipe_id")  # Use get method to avoid KeyError
    print("Recipe ID from form:", recipe_id)  # Add this line for debugging


    if not Comment.form_is_valid(request.form):
        flash("Comment form is not valid.")
        return redirect(f"/recipes/{recipe_id}")

    try:
        Comment.create(request.form)
        flash("Comment created successfully.")
    except Exception as e:
        flash(f"Error occurred while creating the comment: {str(e)}")

    return redirect(f"/recipes/{recipe_id}")


@app.post("/comments/<int:comment_id>/delete")
def comment_delete(comment_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    comment_id = request.form["comment_id"]
    recipe_id = request.form["recipe_id"]

    Comment.delete_comment(comment_id)

    return redirect(f"/recipes/{recipe_id}")