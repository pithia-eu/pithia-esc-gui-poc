class ValidationError(Exception):
    def __init__(self, message, details) -> None:
        super().__init__(message)
        self.message = message
        self.details = details

class InvalidResourceURL(ValidationError):
    pass

class UnregisteredResourceReferenced(ValidationError):
    pass

class UnregisteredOntologyTermReferenced(ValidationError):
    pass

class InvalidRootElementName(ValidationError):
    pass

class FileNameNotMatchingWithLocalID(ValidationError):
    pass

class FileRegisteredBefore(ValidationError):
    pass