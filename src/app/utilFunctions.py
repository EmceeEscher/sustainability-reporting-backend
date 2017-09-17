from app import errorCodes
from flask import jsonify

def getJsonErrrorFromSQL(sqlError):
    errorString = sqlError.to_dict()['message']
    errorBody = {}
    errorBody['code'] = errorCodes.unknownSqlError
    errorBody['message'] = 'Unknown database error'
    # The following line is only to be used for debugging. It should be commented out for production
    # errorBody['SQL message'] = errorString
    
    if "duplicate key value" in errorString:
        errorBody['code'] = errorCodes.duplicateKeyError
        errorBody['message'] = 'An item with that key already exists in the database'

    errorWrapper = {}
    errorWrapper['error'] = errorBody
    response = jsonify(errorWrapper)
    response.status_code = sqlError.status_code
    return response