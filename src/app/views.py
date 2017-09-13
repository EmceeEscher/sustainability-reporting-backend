from app import app
from app import dbFunctions
from flask import request
from flask import jsonify

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/tables', methods=['POST'])
def createDbTables():
    return dbFunctions.initializeTable()

@app.route('/tables', methods=['DELETE'])
def deleteDbTables():
    return dbFunctions.deleteTables()

@app.route('/users', methods=['POST'])
def addUser():
    userId = request.args.get('userId')
    username = request.args.get('username')
    unit = request.args.get('unit')
    adminLevel = request.args.get('adminLevel')
    return dbFunctions.addUser(userId, username, unit, adminLevel)

@app.route('/users', methods=['GET'])
def getUsers():
    data = dbFunctions.getUsers()
    jsonableData = list(map(lambda user: user.__dict__, data))
    return jsonify(data=jsonableData)

@app.route('/users/<userId>', methods=['GET'])
def getUser(userId):
    data = dbFunctions.getUser(userId)
    return jsonify(data=data.__dict__)

@app.route('/units', methods=['POST'])
def addUnit():
    name = request.args.get('name')
    description = request.args.get('description')
    adminId = request.args.get('adminId')
    return dbFunctions.addUnit(name, description, adminId)
