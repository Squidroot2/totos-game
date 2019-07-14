class Log:
    instance = None
    """Component Class of Player"""
    def __init__(self, owner):
        self.owner = owner
        self.messages = []
        self.setInstance(self)

    def getLastMessages(self, num):
        """Gets the last messages written to the Log"""
        return self.messages[-num:]

    @classmethod
    def setInstance(cls, instance):
        cls.instance = instance

    @classmethod
    def addMessage(cls, message):
        cls.instance.messages.append(message)
