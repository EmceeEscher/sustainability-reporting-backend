def initErrorCodes():
    global duplicateKeyError
    global duplicateTableError
    global missingEntryError
    global missingValueError
    global invalidValueError
    global unknownSqlError
    global missingParentEntryError

    duplicateKeyError = 4000
    duplicateTableError = 4001
    missingEntryError = 4002
    missingValueError = 4003
    invalidValueError = 4004
    missingParentEntryError = 4005
    unknownSqlError = 5000