

class Producer():

    def __init__(self, value=0, amount=0, cost=0):
        self.attributes = {"value":value, "amount":amount, "cost":cost}

    def buy(self, amount):
        self.attributes["amount"] += 1

    def return_amount(self):
        return str(self.attributes["amount"])

    def return_cost(self):
        return str(self.attributes["cost"])

    def update_cost(self):
        self.attributes["cost"] = self.attributes["cost"] * (self.attributes["amount"] + 1)
