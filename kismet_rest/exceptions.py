"""All exceptions for the kismet-rest library are defined here."""


class KismetConnectorException(Exception):
    """General class."""



class KismetLoginException(KismetConnectorException):
    """Authentication-related exception."""
    def __init__(self, message, rcode):
        super(Exception, self).__init__(message)
        self.rcode = rcode


class KismetRequestException(KismetConnectorException):
    """Request-related exception."""
    def __init__(self, message, rcode):
        super(Exception, self).__init__(message)
        self.rcode = rcode


class KismetConnectionError(KismetConnectorException):
    """Connection-related exception."""
    def __init__(self, message, rcode=None):
        super(Exception, self).__init__(message)
        self.rcode = rcode

class KismetServiceError(KismetConnectorException):
    """Server-side application errors."""
    def __init__(self, message, rcode):
        super(Exception, self).__init__(message)
        self.rcode = rcode
