from flask_app import DB
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.controllers import user_controller
from flask_app.models.user_model import User
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Entry:
    def __init__(self, data):
        self.id = data["id"]
        self.attendance_date = data["attendance_date"]
        self.attendance = data["attendance"]
        self.reason = data["reason"]
        self.comments = data["comments"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users_id = data["users_id"]
        self.owner = None # there can be one owner set to None
    
    @classmethod
    def get_all_entries_with_users(cls):
        query = "SELECT * FROM entries LEFT JOIN users ON users.id = entries.users_id"

        result = connectToMySQL(DB).query_db(query)
        print(result)
        entry_join_user = []
        for serve in result:
            data = cls(serve)
            userinfo = {
            'id': serve['users.id'],
            'first_name': serve['first_name'],
            'last_name': serve['last_name'],
            'email': serve['email'],
            'password': None,
            'created_at': serve['users.created_at'],
            'updated_at': serve['users.updated_at']
            }
            data.owner = User(userinfo)
            print(data)
            entry_join_user.append(data)
        return entry_join_user


#Create
    @classmethod
    def save(cls, data):
        query = "INSERT INTO entries (attendance_date, attendance, reason, comments, users_id) VALUES (%(attendance_date)s,%(attendance)s,%(reason)s,%(comments)s,%(user_id)s);"

        # comes back as the new row id
        result = connectToMySQL(DB).query_db(query,data)
        return result
    
    @staticmethod
    def validate_entries(data):
        is_valid = True
        print(data)
        if len(data['attendance_date']) < 2:
            flash("Attendance Date Needs To Be Entered", "new_Entries")
            is_valid = False
        
        if 'attendance' not in data or data['attendance'] not in ['yes', 'no']:
            flash("Will you be in attendance? Please select 'Yes' or 'No'", "new_Entries")
            is_valid = False
        
        if len(data['reason']) < 1:
            flash("Put NA if you are attending Church", "new_Entries")
            is_valid = False
        
        if len(data['comments']) < 1:
            flash("Put NA if you don't have comments", "new_Entries")
            is_valid = False
        return is_valid
    
    #Edit Page
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM entries LEFT JOIN users ON users.id = entries.users_id WHERE entries.id = %(id)s;"

        result = connectToMySQL(DB).query_db(query, data)

        entry = result[0]
        one_entry = cls(entry)
        userinfo = {
            'id': entry['users.id'],
            'first_name': entry['first_name'],
            'last_name': entry['last_name'],
            'email': entry['email'],
            'password': None,
            'created_at': entry['users.created_at'],
            'updated_at': entry['users.updated_at']
        }
        one_entry.owner = User(userinfo)
        return one_entry
    
    #Updating Page
    @classmethod
    def edit_one(cls, data):
        query = "UPDATE entries SET attendance_date = %(attendance_date)s, attendance = %(attendance)s, reason = %(reason)s, comments = %(comments)s WHERE entries.id = %(id)s;"

        connectToMySQL(DB).query_db(query, data)
        return True
    
    #Delete
    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM entries WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)
    