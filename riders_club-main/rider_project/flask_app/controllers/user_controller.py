from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Main Page Log/Reg

@app.route('/')
def index():
    return render_template("logreg.html")

@app.route('/register', methods=['POST'])
def main_page():
    if not User.validate_user(request.form):
        return redirect('/')
    
    updated_form = User.generate_pass_for_new_user(request.form)
    print(updated_form)
    user_id = User.save(updated_form)
    session["user_id"] = user_id
    session["first_name"] = request.form["first_name"]
    return redirect("/dashboard")

@app.route('/login', methods=["POST"])
def login_dashboard():
    if not User.validate_login(request.form):
        return redirect('/')
    new_user = User.get_email(request.form["email"])

    session["user_id"] = new_user.id
    session["first_name"] = new_user.first_name
    # return request.form
    return redirect("/dashboard")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
