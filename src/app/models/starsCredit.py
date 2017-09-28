class StarsCredit:
    """A model for the STARS credit entity in the Postgres database (a subtype of the action entity"""

    def __init__(self, actionId, title, description, stakeholderId, theme, priorityArea, creditId, approvalStatus, date):
        self.actionId = actionId
        self.title = title
        self.description = description
        self.stakeholderId = stakeholderId
        self.theme = theme
        self.priorityArea = priorityArea
        self.creditId = creditId
        self.approvalStatus = approvalStatus
        self.date = date