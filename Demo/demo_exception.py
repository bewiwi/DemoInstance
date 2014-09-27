class DemoException(Exception):
    def __init__(self):
        self.value = "ERROR DEMO"
    def __str__(self):
        return repr(self.value)


class DemoExceptionToMuchInstance(DemoException):
    def __init__(self):
        self.value = "To much instances"
    def __str__(self):
        return repr(self.value)