class StarsCredit:
    """A model for the STARS credit entity in the Postgres database (a subtype of the action entity"""

    def __init__(self, actionId, title, description, stakeholderId, theme, priorityArea, creditId, approvalStatus, year):
        self.actionId = actionId
        self.title = title
        self.description = description
        self.stakeholderId = stakeholderId
        self.theme = theme
        self.priorityArea = priorityArea
        self.creditId = creditId
        self.approvalStatus = approvalStatus
        self.year = year