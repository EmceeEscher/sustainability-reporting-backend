
class User:
    """A model for the User entity in the Postgres database"""

    def __init__(self, username, unit, adminLevel):
        self.username = username
        self.unit = unit
        self.adminLevel = adminLevel