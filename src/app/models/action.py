class Action:
    """A model for the action entity in the Postgres database"""

    def __init__(self, actionId, title, description, stakeholderId, theme, priorityArea):
        self.actionId = actionId
        self.title = title
        self.description = description
        self.stakeholderId = stakeholderId
        self.theme = theme
        self.priorityArea = priorityArea
