from app import errorCodes
from flask import jsonify
import re

def getJsonErrrorFromSQL(sqlError):
    errorString = sqlError.to_dict()['message']
    errorBody = {}
    errorBody['code'] = errorCodes.unknownSqlError
    errorBody['message'] = 'Unknown database error'

    httpCode = sqlError.status_code
    # The following line is only to be used for debugging. It should be commented out for production
    errorBody['SQL message'] = errorString

    if bool(re.search("duplicate key value", errorString)):
        errorBody['code'] = errorCodes.duplicateKeyError
        errorBody['message'] = 'An item with that key already exists in the database'

    if bool(re.search("relation .* already exists", errorString)):
        errorBody['code'] = errorCodes.duplicateTableError
        errorBody['message'] = 'A table with that name already exists in the database'

    if bool(re.search("No entry found", errorString)):
        errorBody['code'] = errorCodes.missingEntryError
        errorBody['message'] = 'No entry with that ID exists in the database'
        httpCode = 404

    if bool(re.search("null value in column .* violates not-null constraint", errorString)):
        errorBody['code'] = errorCodes.missingValueError
        errorBody['message'] = 'Missing required field: ' + re.search('column \"(.*)\" violates', errorString).group(1)

    errorWrapper = {}
    errorWrapper['error'] = errorBody
    response = jsonify(errorWrapper)
    response.status_code = httpCode
    return response