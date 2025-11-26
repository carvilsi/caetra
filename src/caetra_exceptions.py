
# Exception raised on Shield configuration issues.
class ShieldConfigurationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Exception raised on general configuration issues.
class ConfigurationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# Reached max actions; not sending.
class MaxActionReached(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# Reached max tries
class MaxRetriesReached(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
