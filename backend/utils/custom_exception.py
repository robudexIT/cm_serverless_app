
class CustomHTTPException(Exception):
    def __init__(self, message, http_status_code):
        super().__init__(message)
        self.http_status_code = http_status_code


