from datetime import datetime
datetime.now()

class API:

    def __init__(self):
        self.log = []
        self.counter = 0

    def update(self):
        a = datetime.now()
        