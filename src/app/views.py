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

# user endpoints

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

@app.route('/users/<userId>/actions', methods=['GET'])
def getImportantActionsByUser(userId):
    data = dbFunctions.getImportantActionsByUser(userId)
    jsonableData = list(map(lambda action: action.__dict__, data))
    return jsonify(data=jsonableData)

@app.route('/users/<userId>/actions/<actionId>', methods=['POST'])
def addImportantActionToUser(userId, actionId):
    response = dbFunctions.addImportantAction(userId, actionId)
    if response == 'OK':
        return response
    else:
        raise DbException(response)

@app.route('/users/<userId>/actions/<actionId>', methods=['DELETE'])
def removeImportantActionFromUser(userId, actionId):
    response = dbFunctions.removeImportantAction(userId, actionId)
    if response == 'OK':
        return response
    else:
        raise DbException(response)

# unit endpoints

@app.route('/units', methods=['POST'])
def addUnit():
    name = request.args.get('name')
    description = request.args.get('description')
    response = dbFunctions.addUnit(name, description)
    if response == 'OK':
        return response
    else:
        raise DbException(response)

@app.route('/units', methods=['GET'])
def getUnits():
    data = dbFunctions.getUnits()
    jsonableData = list(map(lambda unit: unit.__dict__, data))
    return jsonify(data=jsonableData)

@app.route('/units/<unitId>', methods=['GET'])
def getUnit(unitId):
    data = dbFunctions.getUnit(unitId)
    return jsonify(data=data.__dict__)

@app.route('/units/<unitId>/admins/<adminId>', methods=['POST'])
def addAdminToUnit(unitId, adminId):
    response = dbFunctions.addUnitAdmin(unitId, adminId)
    if response == 'OK':
        return response
    else:
        raise DbException(response)

# action endpoints
@app.route('/actions', methods=['POST'])
def addAction():
    title = request.args.get('title')
    description = request.args.get('description')
    stakeholderId = request.args.get('stakeholderId')
    theme = request.args.get('theme')
    priorityArea = request.args.get('priorityArea')
    response = dbFunctions.addAction(title, description, stakeholderId, theme, priorityArea)
    if response == 'OK':
        return response
    else:
        raise DbException(response)

@app.route('/actions', methods=['GET'])
def getActions():
    data = dbFunctions.getActions()
    jsonableData = list(map(lambda action: action.__dict__, data))
    return jsonify(data=jsonableData)

@app.route('/actions/<actionId>', methods=['GET'])
def getAction(actionId):
    data = dbFunctions.getAction(actionId)
    return jsonify(data=data.__dict__)

# metric endpoints
@app.route('/metrics', methods=['POST'])
def addMetric():
    title = request.args.get('title')
    description = request.args.get('description')
    stakeholderId = request.args.get('stakeholderId')
    approvalStatus = request.args.get('approvalStatus')
    value = request.args.get('value')
    textValue = request.args.get('textValue')
    response = dbFunctions.addMetric(title, description, stakeholderId, approvalStatus, textValue, value)
    if response == 'OK':
        return response
    else:
        raise DbException(response)

@app.route('/metrics', methods=['GET'])
def getMetrics():
    data = dbFunctions.getMetrics()
    jsonableData = list(map(lambda metric: metric.__dict__, data))
    return jsonify(data=jsonableData)

@app.route('/metrics/<metricId>', methods=['GET'])
def getMetric(metricId):
    data = dbFunctions.getMetric(metricId)
    return jsonify(data=data.__dict__)

@app.route('/metrics/<metricId>', methods=['PATCH'])
def updateMetric(metricId):
    newValue = request.args.get('value')
    newDescription = request.args.get('description')
    newStakeholderId = request.args.get('stakeholderId')
    newApprovalStatus = request.args.get('approvalStatus')
    newTextValue = request.args.get('textValue')
    response = dbFunctions.updateMetric(metricId, newValue, newTextValue, newDescription, newStakeholderId, newApprovalStatus)
    if response == 'OK':
        return response
    else:
        raise DbException(response)

@app.errorhandler(DbException)
def handle_invalid_usage(error):
    return utilFunctions.getJsonErrrorFromSQL(error)