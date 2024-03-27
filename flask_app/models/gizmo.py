from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Gizmo:
    DB = "database_name"

    def __init__(self, data):
        self.id = data["id"]
        self.column1 = data["column1"]
        self.column2 = data["column2"]
        self.column3 = data["column3"]
        self.column4 = data["column4"]
        self.column5 = data["column5"]
        self.create_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):
        is_valid = True

        # Text Validator
        if len(form_data["column"]) == 0:
            flash("Please enter column.")
            is_valid = False
        elif len(form_data["column"]) < 3:
            flash("Column must be at least three characters.")
            is_valid = False

        # Data Validator
        if len(form_data["date_column"]) == 0:
            flash("Please enter date_column.")
            is_valid = False
        else:
            try:
                datetime.strptime(form_data["date_column"], "%Y-%m-%d")
            except:
                flash("Invalid data_column.")
                is_valid = False

        # Radio Button Validator
        if "radio_column" not in form_data:
            flash("Please enter radio_column.")
            is_valid = False
        elif form_data["radio_column"] not in ["choice1", "choice2"]:
            flash("radio_column must be at least three characters.")
            is_valid = False

        return is_valid

    @classmethod
    def find_all(cls):