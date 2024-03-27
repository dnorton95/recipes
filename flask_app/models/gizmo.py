from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Gizmo:
    DB = "test_db"

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
                flash("Invalid date_column.")
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
        query = """SELECT * FROM gizmos JOIN users ON gizmos.user_id = users.id"""
        list_of_dicts = connectToMySQL(Gizmo.DB).query_db(query)

        gizmos = []
        for each_dict in list_of_dicts:
            gizmo = Gizmo(each_dict)
            gizmos.append(gizmo)
        return gizmos
    
    @classmethod
    def find_all_with_users(cls):
        query = """SELECT * FROM gizmos JOIN users ON gizmos.user_id = users.id"""

        list_of_dicts = connectToMySQL(Gizmo.DB).query_db(query)

        gizmos = []
        for each_dict in list_of_dicts:
            gizmo = Gizmo(each_dict)
            user_data = {
                "id": each_dict["gizmos.id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["gizmos.created_at"],
                "updated_at": each_dict["gizmos.updated_at"],
            }
            user = User(user_data)
            gizmo.user = user
            gizmos.append(gizmo)
        return gizmos
    
    @classmethod
    def find_by_id(cls, gizmo_id):
        query = """SELECT * FROM gizmos WHERE id = %(gizmo_id)s"""
        data = {"gizmo_id": gizmo_id}
        list_of_dicts = connectToMySQL(Gizmo.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        gizmo = Gizmo(list_of_dicts[0])
        return gizmo
    
    @classmethod
    def find_by_id_with_user(cls, gizmo_id):
        query = """SELECT * FROM gizmos JOIN users ON gizmos.user_id = users.id 
        WHERE gizmos.id = %(gizmo_id)s"""

        data = {"gizmo_id": gizmo_id}
        list_of_dicts = connectToMySQL(Gizmo.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        gizmo = Gizmo(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        gizmo.user = User(user_data)
        return gizmo
    
    @classmethod
    def create(cls, form_data):
        query = """INSERT INTO gizmos
        (column1, column2, column3, column4, column5, user_id)
        VALUES
        (%(column1)s, %(column2)s, %(column3)s, %(column4)s, %(column5)s, 
        %(user_id)s,)"""
        gizmo_id = connectToMySQL(Gizmo.DB).query_db(query, form_data)
        return gizmo_id
    
    @classmethod
    def update(cls, form_data):
        query = """UPDATE gizmos
        SET
        column1=%(column1)s,
        column2=%(column2)s,
        column3=%(column3)s,
        column4=%(column4)s,
        column5=%(column5)s,
        WHERE id = %(gizmo_id)s;"""
        connectToMySQL(Gizmo.DB).query_db(query, form_data)
        return
    
    @classmethod
    def delete_by_id(cls, gizmo_id):
        query = """DELETE FROM gizmos WHERE id = %(gizmo_id)s;"""
        data = {"gizmo_id": gizmo_id}
        connectToMySQL(Gizmo.DB).query_db(query, data)
        return