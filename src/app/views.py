from app import app
from app import dbFunctions
from app import utilFunctions
from flask import request
from flask import jsonify
from .exceptions.dbException import DbException

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/tables', methods=['POST'])
def createDbTables():
    response = dbFunctions.initializeTables()
    if response == 'OK':
        return response
    else:
        raise DbException(response)

@app.route('/tables', methods=['DELETE'])
def deleteDbTables():
    return dbFunctions.deleteTables()

@app.route('/users', methods=['POST'])
def addUser():
    userId = request.args.get('userId')
    username = request.args.get('username')
    unit = request.args.get('unit')
    adminLevel = request.args.get('adminLevel')
    response = dbFunctions.addUser(userId, username, unit, adminLevel)
    if response == 'OK':
        return response
    else:
        raise DbException(response)

@app.route('/users', methods=['GET'])
def getUsers():
    data = dbFunctions.getUsers()
    jsonableData = list(map(lambda user: user.__dict__, data))
    return jsonify(data=jsonableData)

@app.route('/users/<userId>', methods=['GET'])
def getUser(userId):
    data = dbFunctions.getUser(userId)
    return jsonify(data=data.__dict__)

@app.route('/users/<userId>/units/<unitId>', methods=['PUT'])
def addUserToUnit(userId, unitId):
    response = dbFunctions.addUserToUnit(userId, unitId)
    if response == 'OK':
        return response
    else:
        raise DbException(response)

@app.route('/units', methods=['POST'])
def addUnit():
    name = request.args.get('name')
    description = request.args.get('description')
    adminId = request.args.get('adminId')
    return dbFunctions.addUnit(name, description, adminId)

@app.errorhandler(DbException)
def handle_invalid_usage(error):
    return utilFunctions.getJsonErrrorFromSQL(error)