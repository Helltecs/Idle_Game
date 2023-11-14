from producers import Producer

class Upgrade():
    def __init__(self, linked_producer: Producer):
        self.linked_producer = linked_producer
        self.cost = self.linked_producer.attributes["cost"] * 50

    def upgrade(self):
        self.linked_producer.attributes["value"] *= 2
        self.cost = self.cost * 5
