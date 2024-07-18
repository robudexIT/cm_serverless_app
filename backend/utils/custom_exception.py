class CustomError(Exception):
    def __init__(self, message, http_status_code=None, details=None):
        super().__init__(message)
        self.http_status_code = http_status_code
        self.details = details


