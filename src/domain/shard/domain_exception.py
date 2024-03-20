

class DomainException(Exception):
    def __init__(self, arg=""):
        self.arg = arg
