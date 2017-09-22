class Metric:
    """A model for the metric entity in the Postgres database"""

    def __init__(self, metricId, title, description, stakeholderId, approvalStatus, value, textValue):
        self.metricId = metricId
        self.title = title
        self.description = description
        self.stakeholderId = stakeholderId
        self.approvalStatus = approvalStatus
        self.value = value
        self.textValue = textValue