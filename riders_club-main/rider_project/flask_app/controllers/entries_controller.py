from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.entries_model import Entry

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/dashboard')
def dashboard_page():
    if 'user_id' not in session:
        return redirect('/')
    dashboard_user = User.info(session["user_id"])
    all_entries = Entry.get_all_entries_with_users()
    print(all_entries[0].users_id)
    print(session['user_id'])
    return render_template("dashboard.html", user_info = dashboard_user, all_entries = all_entries)


#Creating the create route
@app.route('/entries')
def show_entries():
    if 'user_id' not in session:
        return redirect('/')
    create_user = User.info(session["user_id"])

    return render_template("create.html", user_info = create_user)

#Creating new Entry
@app.route('/entries/new', methods=['POST'])
def create():
    if 'user_id' not in session:
        return redirect('/')
    print(request.form)
    if not Entry.validate_entries(request.form):
        return redirect('/entries')
    Entry.save(request.form)
    save_entry = User.info(session["user_id"])
    return redirect("/dashboard")

#Editing Page
@app.route('/entries/edit/<int:id>')
def edit_page(id):
    if 'user_id' not in session:
        return redirect('/')
    view_user = User.info(session["user_id"])
    data ={
        'id' : id
    }
    entries = Entry.get_one(data)
    return render_template('edit.html', user_info = view_user, entries = entries )

#Update Page
@app.route('/entries/edit_page/<int:id>', methods=['POST'])
def edit_entry(id):
    if 'user_id' not in session:
        return redirect('/')
    print(request.form)
    if not Entry.validate_entries(request.form):
        return redirect(f'/entries/edit/{id}')
    Entry.edit_one(request.form)
    save_Entry = User.info(session["user_id"])

    return redirect('/dashboard')

#Show Page
@app.route('/entries/show/<int:id>')
def show__one_entry(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id' : id
    }
    
    entries = Entry.get_one(data)
    return render_template('view.html', entries = entries)

#Destroy Entry
@app.route('/entries/destroy/<int:id>')
def destroy_entry(id):
    data ={
        'id': id
    }
    Entry.destroy(data)
    return redirect('/dashboard')
