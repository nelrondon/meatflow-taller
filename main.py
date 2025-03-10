# DEPENDENCIAS EXTERNAS
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# DEPENDENCIAS INTERNAS
from components import *

class MainApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.user = {
            "user": None,
            "name": tk.StringVar()
        }

        # Datos generales
        self.num_clientes = tk.IntVar()
        self.num_productos = tk.IntVar()
        self.num_proveedores = tk.IntVar()
        self.num_compras = tk.IntVar()
        self.num_ventas = tk.IntVar()

        # Datos de Ventas
        self.ventas_efe = tk.StringVar()
        self.ventas_trans = tk.StringVar()
        self.ventas_card = tk.StringVar()

        # Datos de inventario
        self.productos_min_stock = Inventario().verifyMinStock()
        self.num_productos_min_stock = tk.IntVar()
        self.updateDashboard()

        #? INTERFAZ
        self.ventana.title("Sistema de Gestión Financiera - MeatFlow")
        self.ventana.geometry("1280x700")
        self.ventana.option_add("*Font", ("Inter", 10))
        self.ventana.iconbitmap("assets/favicon.ico")
        self.ventana.withdraw()

        #VENTANAS
        loginForm = LoginForm(self)
        changePasswForm = ChangePasswForm(self)
        stockForm = StockForm(self)
        buyForm = BuyForm(self)
        clientForm = Client(self)
        reportForm = ReporteForm(self)

        #? MENÚ DE NAVEGACIÓN
        nav_menu = tk.Menu(self.ventana)
        self.ventana.config(menu=nav_menu)

        #? MENU
        file_menu = tk.Menu(nav_menu, tearoff=0)
        file_menu.add_command(label="Cerrar Sesión", command=self.handle_main_quit)
        file_menu.add_command(label="Configuración")
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.handle_main_quit)

        user_menu = tk.Menu(nav_menu, tearoff=0)
        user_menu.add_command(label="Perfil")
        user_menu.add_command(label="Cambiar Contraseña", command=changePasswForm.show)

        nav_menu.add_cascade(label="Archivo", menu=file_menu)
        nav_menu.add_cascade(label="Usuario", menu=user_menu)

        #? CUERPO DE LA INTERFAZ
        # - LADO MENU
        self.menu = tk.Frame(self.ventana, width=300, bd=1, relief="ridge")
        # Logo
        self.logo = Image.open("assets/logo.png")
        self.logo_tk = ImageTk.PhotoImage(self.logo)
        labelImage = tk.Label(self.menu, image=self.logo_tk)
        labelImage.pack(pady=(50, 20))

        self.botones = tk.Frame(self.menu)

        gap=10
        ttk.Button(self.botones, command=buyForm.show, width=25, text="Registrar compra").pack(pady=gap)
        ttk.Button(self.botones, command=clientForm.show, width=25, text="Registrar venta").pack(pady=gap)
        ttk.Button(self.botones, command=stockForm.show, width=25, text="Ver inventario").pack(pady=gap)
        ttk.Button(self.botones, command=None, width=25, text="Generar reporte").pack(pady=gap)

        self.botones.pack()

        ttk.Button(self.menu, width=25, text="Cerrar Sesión", command=self.handle_main_quit
        ).pack(side="bottom", pady=(0, 50))

        self.menu.pack_propagate(False)
        self.menu.pack(side="left", fill=tk.Y)


        # - LADO PANTALLA
        self.display = tk.Frame(self.ventana) 
        self.display.pack_propagate(False)
        self.display.pack(side="left", fill=tk.BOTH, expand=True)

        tk.Label(self.display, text="Dashboard", font=("Inter Bold", 30), foreground=COLOR1
        ).pack(pady=(50, 20))

        info = tk.Frame(self.display)
        info.pack()

        Widget.InputGrid(info, "Clientes registrados", self.num_clientes, [0, 0], width=4, js="center", state="readonly", fs=30, gap=[10, 10])
        Widget.InputGrid(info, "Productos registrados", self.num_productos, [1, 0], width=4, js="center", state="readonly", fs=30, gap=[10, 10])
        Widget.InputGrid(info, "Proveedores registrados", self.num_proveedores, [2, 0], width=4, js="center", state="readonly", fs=30, gap=[10, 10])
        Widget.InputGrid(info, "Compras registradas", self.num_compras, [0, 3], width=4, js="center", state="readonly", fs=30, gap=[10, 10])
        Widget.InputGrid(info, "Ventas registradas", self.num_ventas, [1, 3], width=4, js="center", state="readonly", fs=30, gap=[10, 10])
        Widget.InputGrid(info, "Productos en bajo Stock", self.num_ventas, [1, 3], width=4, js="center", state="readonly", fs=30, gap=[10, 10])

        Widget.InputGrid(info, "Ventas por efectivo", self.ventas_efe, [0, 5], width=4, js="center", state="readonly", fs=30, gap=[10, (50, 20)])
        Widget.InputGrid(info, "Ventas por tranferencia", self.ventas_trans, [1, 5], width=4, js="center", state="readonly", fs=30, gap=[10, (50, 20)])
        Widget.InputGrid(info, "Ventas por tarjeta", self.ventas_card, [2,5], width=4, js="center", state="readonly", fs=30, gap=[10, (50, 20)])


        self.ventana.protocol("WM_DELETE_WINDOW", self.handle_main_quit)

        # Barra de Estado
        stsbar = tk.Frame(self.display, bd=1, relief=tk.SUNKEN)
        ttk.Label(stsbar, text="Bienvenido, ").grid(column=0, row=0)
        ttk.Label(stsbar, textvariable=self.user["name"]).grid(column=1, row=0)
        stsbar.pack(side=tk.BOTTOM, fill=tk.X)

    def handle_main_quit(self):
        answ = messagebox.askyesno(
            title="Estás a punto de salir...", 
            message="Deseas cerrar sesion y salir del sistema?"
        )
        if answ:
            self.ventana.destroy()

    def updateDashboard(self):
        # Datos generales
        self.num_clientes.set(len(DB.get("clientes")))
        self.num_productos.set(len(DB.get("productos")))
        self.num_proveedores.set(len(DB.get("proveedores")))
        self.num_compras.set(len(DB.get("compras")))
        self.num_ventas.set(len(DB.get("ventas")))

        # Datos de ventas
        self.ventas_efe.set(len(Venta.filter_by_payment_method("efectivo")))
        self.ventas_trans.set(len(Venta.filter_by_payment_method("transferencia")))
        self.ventas_card.set(len(Venta.filter_by_payment_method("tarjeta")))

         # Datos de inventario
        self.productos_min_stock = Inventario().verifyMinStock()
        self.num_productos_min_stock.set(len(self.productos_min_stock))

    def render(self):
        self.ventana.resizable(False, False)
        self.ventana.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.render()