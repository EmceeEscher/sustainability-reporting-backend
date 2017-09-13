from app import app
from app import dbFunctions
from flask import request
from flask import jsonify

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

@app.route('/users', methods=['GET'])
def getUsers():
    data = dbFunctions.getUsers()
    jsonableData = list(map(lambda user: user.__dict__, data))
    return jsonify(data=jsonableData)

@app.route('/users/<userId>', methods=['GET'])
def getUser(userId):
    data = dbFunctions.getUser(userId)
    return jsonify(data=data.__dict__)

@app.route('/tables', methods=['POST'])
def createDbTables():
    dbFunctions.initializeTable()
    return 'OK'

@app.route('/tables', methods=['DELETE'])
def deleteDbTables():
    dbFunctions.deleteTables()
    return 'OK'
