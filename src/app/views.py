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

# TODO remove all /tables endpoints before productionization
@app.route('/tables', methods=['POST'])
def createDbTables():
    response0 = dbFunctions.initializeTypes()
    response1 = dbFunctions.initializeTables()
    if ((response1 == 'OK') and (response0 == 'OK')) :
        return response1
    elif (response0 == 'OK'):
        raise DbException(response1)
    else:
        raise DbException(response0)

@app.route('/tables/new', methods=['POST'])
def createNewTables():
    response = dbFunctions.initializeNewTables()
    if response == 'OK':
        return response
    else:
        raise DbException(response)

@app.route('/tables', methods=['DELETE'])
def deleteDbTables():
    response0 = dbFunctions.deleteTables()
    response1 = dbFunctions.deleteTypes()
    if ((response1 == 'OK') and (response0 == 'OK')) :
        return response1
    elif (response0 == 'OK'):
        raise DbException(response1)
    else:
        raise DbException(response0)

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
    return dbFunctions.addUnit(name, description)

@app.route('/units/<unitId>/admins/<adminId>', methods=['POST'])
def addAdminToUnit(unitId, adminId):
    response = dbFunctions.addUnitAdmin(unitId, adminId)
    if response == 'OK':
        return response
    else:
        raise DbException(response)

@app.errorhandler(DbException)
def handle_invalid_usage(error):
    return utilFunctions.getJsonErrrorFromSQL(error)