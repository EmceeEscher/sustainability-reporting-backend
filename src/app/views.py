from app import app
from app import dbFunctions
from flask import request

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/users', methods=['POST'])
def addUserToDb():
    username = request.args.get('username')
    unit = request.args.get('unit')
    adminLevel = request.args.get('adminLevel')
    dbFunctions.addUser(username, unit, adminLevel)
    return 'OK'