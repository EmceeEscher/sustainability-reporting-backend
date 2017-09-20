class Unit:
    """A model for the Unit entity in the Postgres database"""

    def __init__(self, unitId, name, description):
        self.unitId = unitId
        self.name = name
        self.description = description
