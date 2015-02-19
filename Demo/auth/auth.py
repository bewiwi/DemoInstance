class DemoAuth:
    def __init__(self, config):
        raise NotImplementedError

    #Must return email if ok or False
    def check_auth(self, user, password):
        raise NotImplementedError