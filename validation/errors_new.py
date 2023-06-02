class ValidationError(Exception):
    pass

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