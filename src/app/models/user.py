class User:
    """A model for the User entity in the Postgres database"""

    def __init__(self, userId, username, unitId, adminLevel):
        self.userId = userId
        self.username = username
        self.unitId = unitId
        self.adminLevel = adminLevel
