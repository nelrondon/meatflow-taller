from handledb import DB
from proveedor import Proveedor
import datetime

class Compra:
    def __init__(self, supplier:Proveedor, prod_buy, quality=10, costototal = 0):
        self.date = str(datetime.datetime.now())
        self.products_buy = []
        self.supplier = supplier
        self.quality = quality
        self.costo_total = costototal
        for _ in prod_buy:
            self.products_buy.append({
                "name": _["name"],
                "price_buy": _["price_buy"],
                "amount": _["stock"],
            })

        
    def calcular_costo_total(self):
        
        for product in self.products_buy:
            self.costo_total+=product["price_buy"]*product["stock"]
        
        return self.costo_total

    def evaluar_compra(self):
        evaluacion=(self.quality*0.4)+(self.products_buy*0.2)+(self.supplier.calcPriority()*0.4)

        evaluacion=max(0, min(evaluacion, 5))

        return evaluacion
    
    def es_mala_compra(self, umbral_costo_calidad=2.0):
        if self.quality == 0:
            return True  # Evitar división por cero (calidad 0 es inválida)

        # Calcular la relación costo vs. calidad
        relacion_costo_calidad = self.costo_total / self.quality

        # Determinar si la compra es mala
        return relacion_costo_calidad > umbral_costo_calidad
    
    def register(self):
        DB.save("compras", self.__dict__)
    
    