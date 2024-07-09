#YOUR CODE ALL STARTS HERE! python server.py
#first thing it does is import everythingfrom __init__.py
from flask_app import app
from flask_app.controllers import user_controller
from flask_app.controllers import entries_controller


if __name__=="__main__":
    app.run(debug=True)