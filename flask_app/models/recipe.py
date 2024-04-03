from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Recipe:
    DB = "recipes_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked = data["date_cooked"]
        self.thirty_min = data["thirty_min"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None

    @staticmethod
    def form_is_valid(recipe_input_data):
        is_valid = True
        # Text Validator
        if len(recipe_input_data["name"]) == 0:
            flash("Please enter name.")
            is_valid = False
        elif len(recipe_input_data["name"]) < 3:
            flash("Name must be at least three characters.")
            is_valid = False

        if len(recipe_input_data["description"]) == 0:
            flash("Please enter description.")
            is_valid = False
        elif len(recipe_input_data["description"]) < 3:
            flash("Description field must be at least three characters.")
            is_valid = False

        if len(recipe_input_data["instructions"]) == 0:
            flash("Please enter instruction.")
            is_valid = False
        elif len(recipe_input_data["instructions"]) < 3:
            flash("Instructions field must be at least three characters.")
            is_valid = False

                # Date Validator
        if len(recipe_input_data["date_cooked"]) == 0:
            flash("Please enter date cooked.")
            is_valid = False
        else:
            try:
                date_cooked=datetime.strptime(recipe_input_data["date_cooked"], "%Y-%m-%d")
            except:
                flash("Please enter in mm/dd/yyyy format.")
                is_valid = False

        # Radio Button Validator
        if "thirty_min" not in recipe_input_data:
            flash("Please enter 30 minute option.")
            is_valid = False
        elif recipe_input_data["thirty_min"] not in ["yes", "no"]:
            flash("30 minute option must be at least three characters.")
            is_valid = False

        return is_valid

    @classmethod
    def find_all_recipes(cls):
        query = """SELECT * FROM recipes JOIN users ON recipes.user_id = users.id"""
        list_of_dicts = connectToMySQL(Recipe.DB).query_db(query)

        recipes = []
        for each_dict in list_of_dicts:
            recipe = Recipe(each_dict)
            recipes.append(recipe)
        return recipes
    
    @classmethod
    def find_all_recipes_with_users(cls):
        query = """SELECT * FROM recipes JOIN users ON recipes.user_id = users.id"""

        list_of_dicts = connectToMySQL(Recipe.DB).query_db(query)

        recipes = []
        for each_dict in list_of_dicts:
            recipe = Recipe(each_dict)
            user_input_data = {
                "id": each_dict["id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["created_at"],
                "updated_at": each_dict["updated_at"],
            }
            user = User(user_input_data)
            recipe.user = user
            recipes.append(recipe)
        return recipes
    
    @classmethod
    def find_recipe_by_id(cls, recipes_id):
        """this method finds a recipe by the ID"""
        query = """SELECT * FROM recipes WHERE id = %(recipes_id)s"""
        data = {"recipes_id": recipes_id}
        list_of_dicts = connectToMySQL(Recipe.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        recipe = Recipe(list_of_dicts[0])
        return recipe
    
    @classmethod
    def find_recipe_by_id_with_user(cls, recipes_id):
        """This method find a recipe by the id and user by the record id"""
        query = """
            SELECT recipes.*, users.*
            FROM recipes
            JOIN users ON recipes.user_id = users.id 
            WHERE recipes.id = %(recipes_id)s
        """

        data = {"recipes_id": recipes_id}
        list_of_dicts = connectToMySQL(Recipe.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        recipe = Recipe(list_of_dicts[0])
        user_input_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        recipe.user = User(user_input_data)
        return recipe


    
    @classmethod
    def new_recipe(cls, recipe_input_data):
        try:
            # Insert recipe data into the recipes table
            query_recipe = """
            INSERT INTO recipes
            (name, description, instructions, date_cooked, thirty_min, user_id)
            VALUES
            (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(thirty_min)s, %(user_id)s)
            """
            recipes_id = connectToMySQL(cls.DB).query_db(query_recipe, recipe_input_data)

            return recipes_id
        except Exception as e:
            # Handle the error
            print(f"An error occurred: {str(e)}")
            return None
        
    @classmethod
    def create(cls, form_data):
        query = """INSERT INTO recipes
        (name, description, instructions, date_cooked, thirty_min, user_id)
        VALUES
        (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(thirty_min)s, 
        %(user_id)s)"""
        recipe_id = connectToMySQL(Recipe.DB).query_db(query, form_data)
        return recipe_id
    
    @classmethod
    def update(cls, recipes_id, recipe_input_data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_cooked = %(date_cooked)s, thirty_min = %(thirty_min)s WHERE id = %(recipes_id)s;"
        data = {
            "recipes_id": recipes_id,
            "name": recipe_input_data["name"],
            "description": recipe_input_data["description"],
            "instructions": recipe_input_data["instructions"],
            "date_cooked": recipe_input_data["date_cooked"],
            "thirty_min": recipe_input_data["thirty_min"]
        }
        connectToMySQL(Recipe.DB).query_db(query, data)
    
    @classmethod
    def delete_by_id(cls, recipes_id):
        query = """DELETE FROM recipes WHERE id = %(recipes_id)s;"""
        data = {"recipes_id": recipes_id}
        connectToMySQL(Recipe.DB).query_db(query, data)
        return
    
    @classmethod
    def count_by_name(cls, name):
        query = """SELECT COUNT(name) AS "count"
        FROM recipes WHERE name = %(name)s"""
        data = {"name": name}
        list_of_dicts = connectToMySQL(Recipe.DB).query_db(query, data)
        print(list_of_dicts)
        return list_of_dicts[0]["count"]