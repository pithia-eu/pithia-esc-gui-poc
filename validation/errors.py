class ValidationError(Exception):
    pass

class FileRegisteredBefore(ValidationError):
    pass

class UpdateFileNotMatching(ValidationError):
    pass