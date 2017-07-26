"""ERRORS"""
class Error(Exception):

    def __init__(self, message):
        self.message = message

    @property
    def serialize(self):
        return {
            'message': self.message
        }

class GeostoreNotFoundError(Error):
    pass

class GeostoreGenericError(Error):
    pass

class FieldsGenericError(Error):
    pass
