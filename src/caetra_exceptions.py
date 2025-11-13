class ShieldConfigurationError(Exception):
    """Exception raised on Shield configuration issues.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ConfigurationError(Exception):
    """Exception raised on general configuration issues.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
