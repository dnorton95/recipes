from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from pprint import pprint


class Comment:
    DB = "recipes_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.recipe_id = data["recipe_id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users = {
            "id": data["users.id"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
        }

    @staticmethod
    def form_is_valid(form_data):
        is_valid = True

        if len(form_data["content"]) == 0:
            flash("Please enter a comment.")
            is_valid = False
        elif len(form_data["content"]) < 3:
            flash("Comment must be at least three characters.")
            is_valid = False

        return is_valid

    @classmethod
    def all_comments(cls, recipe_id):
        data = {"recipe_id": recipe_id}
        query = """SELECT *
                FROM comments
                JOIN users ON comments.user_id = users.id
                WHERE comments.recipe_id = %(recipe_id)s
                ORDER BY comments.created_at DESC; """
        list_of_dicts = connectToMySQL(Comment.DB).query_db(query, data)
        pprint(list_of_dicts)

        comments = []
        for each_dict in list_of_dicts:
            comment = Comment(each_dict)
            comments.append(comment)
        return comments

    @classmethod
    def create(cls, form_data):
        query = """INSERT INTO comments (user_id, recipe_id, content) 
        VALUES (%(user_id)s, %(recipe_id)s, %(content)s);"""
        connectToMySQL("recipes_schema").query_db(query, form_data)
        return

    @classmethod
    def delete_comment(cls, comment_id):
        query = """DELETE FROM comments WHERE id = %(comment_id)s"""
        data = {"comment_id": comment_id}
        connectToMySQL(Comment.DB).query_db(query, data)
        return