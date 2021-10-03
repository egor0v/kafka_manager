class Config():
    _instance = None
    
    host = None
    username = None
    password = None

    def __new__(cls, host, username, password, *args, **kwargs):
        if not Config._instance:
            Config._instance = super(Config, cls).__new__(
                cls, *args, **kwargs
            )
        return Config._instance

    def __init__(self, host, username, password, *args, **kwargs):
        self.host = host
        self.username = username
        self.password = password
