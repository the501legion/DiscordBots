class Quote:
    def __init__(self, data):
        self.id = data[0]
        self.text = data[1]
        self.author = data[2]


EMPTY: Quote = Quote([0, "none", "none"])
