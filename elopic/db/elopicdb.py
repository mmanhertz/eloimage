from tinydb import TinyDB


class EloPicDB:

    def __init__(self):
        self.db = None

    def create(self, path):
        self.db = TinyDB(path)
