class Unit:
    """A model for the Unit entity in the Postgres database"""

    def __init__(self, name, description):
        self.name = name
        self.description = description
