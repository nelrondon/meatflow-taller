from handledb import DB


class Producto:
    def __init__(self, data:dict):
        self.name = data["name"]
        self.category = data["category"]
        self.price_buy = data["price_buy"]
        self.price_sell = data["price_sell"]
        self.exp_date = data["exp_date"]
        self.stock = data["stock"]
        self.type = data["type"]
        self.gain = self.calcGain()

    def register(self):
        DB.save("productos", self.__dict__)

    def setPriceSell(self):
        pass

    def calcGain(self):
        return self.price_sell - self.price_buy

    