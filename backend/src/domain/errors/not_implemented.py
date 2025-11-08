
class NotImplementedHTTPError(Exception):
    def __init__(self, message: str = "Not implemented"):
        self.message = message
