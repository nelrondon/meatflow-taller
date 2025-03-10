from datetime import datetime
from tkinter import messagebox
from handledb import DB

class Inventario:
    def __init__(self):
        self.products = self.load()
        self.products_min_stock = self.verifyMinStock()
    
    def load(self):
        return DB.get("productos")
    
    def search(self, name):
        return DB.getOneBy("productos", "name", name)

    def verifyMinStock(self):
        minStock = 30
        minStockList = []
        for prod in self.products:
            if prod["stock"] < minStock:
                minStockList.append(prod)
        return minStockList

    def alertExpire(self):
        today = datetime.now().date()
        
        threshold = 7
        
        expiring_products = []
        
        for prod in self.products:
            # Convertir la fecha de vencimiento a datetime.date
            exp_date = datetime.strptime(prod["exp_date"], "%Y-%m-%d").date()
            
            # Calcular los días restantes hasta el vencimiento
            days_remaining = (exp_date - today).days
            
            # Si los días restantes son menores o iguales al umbral, agregar el producto a la lista
            if days_remaining <= threshold:
                expiring_products.append({
                    "name": prod["name"],
                    "exp_date": prod["exp_date"],
                    "days_remaining": days_remaining
                })
        
        # Alertar al usuario sobre los productos próximos a caducar
        if expiring_products:
            alert_message = "Los siguientes productos están próximos a caducar:\n"
            for product in expiring_products:
                alert_message += f"- {product['name']} (Vence el {product['exp_date']}, días restantes: {product['days_remaining']})\n"
            messagebox.showwarning("Alerta de Vencimiento", alert_message)
        else:
            messagebox.showinfo("Alerta de Vencimiento", "No hay productos próximos a caducar.")
        return expiring_products

    def trendStock(self):
        pass
