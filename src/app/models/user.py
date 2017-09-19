class User:
    """A model for the User entity in the Postgres database"""

    def __init__(self, username, unitId, adminLevel):
        self.username = username
        self.unitId = unitId
        self.adminLevel = adminLevel
