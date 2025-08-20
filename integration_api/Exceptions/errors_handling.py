class NotFoundException(Exception):
    http_status_code = 404

    def __init__(self, message="Function Method Not Found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message