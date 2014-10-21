class DemoException(Exception):
    def __init__(self):
        self.value = "ERROR DEMO"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionBadConfigValue(DemoException):
    def __init__(self, config, value):
        self.value = "Bad config value for %s : %s" % (config, value)
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionToMuchInstanceImage(DemoException):
    def __init__(self):
        self.value = "To much instances"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionUserAlreadyHaveInstanceImage(DemoException):
    def __init__(self):
        self.value = "User Already have instance"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionInvalidImage(Exception):
    def __init__(self,image_var):
        self.value = "Image Invalid %s" % image_var
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionInvalidImageTime(Exception):
    def __init__(self, time):
        self.value = "Invalid Time %s" % time
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionInvalidOwner(Exception):
    def __init__(self, time):
        self.value = "Invalid Owner"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionUserInstanceTypeAlreadyExist(Exception):
    def __init__(self, time):
        self.value = "User already have an instance of this type"
        self.message = self.value

    def __str__(self):
        return repr(self.value)


class DemoExceptionUserTokenInvalid(Exception):
    def __init__(self, time):
        self.value = "User token is invalid"
        self.message = self.value

    def __str__(self):
        return repr(self.value)