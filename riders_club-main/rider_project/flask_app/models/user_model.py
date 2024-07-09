from flask_app import DB
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.controllers import user_controller
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_entries = [] # many trips so open loop 
    
#Registration methods

    @classmethod
    def get_email(cls, email):
        email_dict = {"email" : email}
        query = " SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query, email_dict)

        if len(result) < 1:
            return False
        found_user = cls(result[0])
        return found_user

    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        
        if len(data['email']) < 5:
            flash("Email must be at least 5 characters", "register")
            is_valid = False

        if len(data['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email")
            is_valid = False

        if data['password'] != data['confirm_pw']:
            flash("Confirm password must match", "register")
            is_valid = False

        if User.get_email(data["email"]):
            flash("This email has already joined us!", "register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def generate_pass_for_new_user(data):
        pw_hash = user_controller.bcrypt.generate_password_hash(data["password"])
        updated_form = {
            "first_name" : data["first_name"],
            "last_name" : data["last_name"],
            "email" : data["email"],
            "password" : pw_hash
        }
        return updated_form
    
    @staticmethod
    def validate_login(data):
        is_valid = True

        new_user = User.get_email(data["email"])
        
        if not new_user:
            print("here in 98")  #testing
            flash("Invalid Email", "login")
            is_valid = False
        
        else:
            if not user_controller.bcrypt.check_password_hash(new_user.password, data["password"]):
                flash("Invalid Password", "login")
                is_valid = False
                print("here in 106") #testing
        return is_valid
    


    #To Save User 

    @classmethod
    def save(cls, form_data):
        query = " INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s );"
        user_id = connectToMySQL(DB).query_db(query, form_data)
        return user_id
    
    #To get info

    @classmethod
    def info(cls,data):
        id_dict = {"id" : data}
        query = " SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, id_dict)
        user_object = User(result[0])
        print("\n\n\n\nline 41 as a user object: ", user_object)
        return user_object