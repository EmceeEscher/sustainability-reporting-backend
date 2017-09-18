class Unit:
    """A model for the Unit entity in the Postgres database"""

    def __init__(self, name, description, adminId):
        self.name = name
        self.description = description
        self.adminId = adminId