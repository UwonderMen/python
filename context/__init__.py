
class Context(dict):
    def __setattr__(self, key, value):
        s