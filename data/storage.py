class Storage:
    def __init__(self, path):
        self.path = path

    def save(self, file):
        with open(f"{self.path}/{file.filename}", "wb") as f:
            f.write(file.read())

    def load(self, filename):
        with open(f"{self.path}/{filename}", "rb") as f:
            return f.read()
