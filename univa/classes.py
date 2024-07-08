class Command():
    def __init__(self, name, description, func, args=None):
        if description == '':
            description = "No description"
        self.name = name
        self.description = description
        self.func = func
        self.args = args

    def execute(self, *args, **kwargs):
        return self.func(*args, **kwargs)