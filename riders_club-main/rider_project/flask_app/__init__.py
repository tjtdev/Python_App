#import your libraries
from flask import Flask
#creating a variable to not have to type Flask(__name__) all the time!
app=Flask(__name__)
app.secret_key = "GroundControlToMajorTom"

DB = "riders_schema"