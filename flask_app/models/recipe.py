from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User_class


class Recipe_class:
    DB = "recipes_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked = data["date_cooked"]
        self.thirty_min = data["thirty_min"]
        self.create_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None

    @staticmethod
    def recipe_is_valid(recipe_input_data):
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
        list_of_dicts = connectToMySQL(Recipe_class.DB).query_db(query)

        recipes = []
        for each_dict in list_of_dicts:
            recipe = Recipe_class(each_dict)
            recipes.append(recipe)
        return recipes
    
    @classmethod
    def find_all_recipes_with_users(cls):
        query = """SELECT * FROM recipes JOIN users ON recipes.user_id = users.id"""

        list_of_dicts = connectToMySQL(Recipe_class.DB).query_db(query)

        recipes = []
        for each_dict in list_of_dicts:
            recipe = Recipe_class(each_dict)
            user_input_data = {
                "id": each_dict["id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["created_at"],
                "updated_at": each_dict["updated_at"],
            }
            user = User_class(user_input_data)
            recipe.user = user
            recipes.append(recipe)
        return recipes
    
    @classmethod
    def find_recipe_by_id(cls, recipe_id):
        """this method finds a recipe by the ID"""
        query = """SELECT * FROM recipes WHERE id = %(recipe_id)s"""
        data = {"recipe_id": recipe_id}
        list_of_dicts = connectToMySQL(Recipe_class.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        recipe = Recipe_class(list_of_dicts[0])
        return recipe
    
    @classmethod
    def find_recipe_by_id_with_user(cls, recipe_id):
        """This method find a recipe by the id and user by the record id"""
        query = """SELECT * FROM recipes JOIN users ON recipes.user_id = users.id 
        WHERE recipes.id = %(recipe_id)s"""

        data = {"recipe_id": recipe_id}
        list_of_dicts = connectToMySQL(Recipe_class.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        recipe = Recipe_class(list_of_dicts[0])
        user_input_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        recipe.user = User_class(user_input_data)
        return recipe
    
    @classmethod
    def new_recipe(cls, recipe_input_data):
        try:
            query = """
            INSERT INTO recipes
            (name, description, instructions, date_cooked, thirty_min, user_id)
            VALUES
            (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(thirty_min)s, %(user_id)s)
            """
            recipe_id = connectToMySQL(cls.DB).query_db(query, recipe_input_data)
            return recipe_id
        except Exception as e:
            # Handle the error
            print(f"An error occurred: {str(e)}")
            return None
    
    @classmethod
    def update(cls, recipe_id, recipe_input_data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_cooked = %(date_cooked)s, thirty_min = %(thirty_min)s WHERE id = %(recipe_id)s;"
        data = {
            "recipe_id": recipe_id,
            "name": recipe_input_data["name"],
            "description": recipe_input_data["description"],
            "instructions": recipe_input_data["instructions"],
            "date_cooked": recipe_input_data["date_cooked"],
            "thirty_min": recipe_input_data["thirty_min"]
        }
        connectToMySQL(Recipe_class.DB).query_db(query, data)
    
    @classmethod
    def delete_by_id(cls, recipe_id):
        query = """DELETE FROM recipes WHERE id = %(recipe_id)s;"""
        data = {"recipe_id": recipe_id}
        connectToMySQL(Recipe_class.DB).query_db(query, data)
        return