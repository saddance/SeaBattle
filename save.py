import shelve

class Save:
    def __init__(self):
        self.file = shelve.open('save')

    def save(self, key, value):
        self.file[key] = value

    def __del__(self):
        self.file.close()
