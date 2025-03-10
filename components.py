import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from auth import AuthUser, Auth
from compra import Compra
from handledb import DB

from producto import Producto
from reporte import Reporte
from cliente import Cliente
from venta import Venta
from inventario import Inventario
from proveedor import Proveedor

COLOR1 = "#225270"
COLOR1_SOFT = "#C4DDED"


class Widget:
    @staticmethod
    def MainLabel(parent, text):
        ttk.Label(parent, text=text,foreground=COLOR1, font=("Inter ExtraBold", 24)
        ).pack(padx=90, pady=(30, 0))

    @staticmethod
    def SecLabel(parent, text):
        ttk.Label(parent, text=text, font=("Inter", 10)
        ).pack()

    @staticmethod
    def Caption(parent, text, side="top"):
        ttk.Label(parent, text=text, foreground=COLOR1, font=("Inter SemiBold", 10)
        ).pack(side=side)
    
    @staticmethod
    def CaptionGrid(parent, text, arr, cspan=1, rspan=1):
        ttk.Label(parent, text=text, foreground=COLOR1, font=("Inter SemiBold", 10)
        ).grid(column=arr[0], row=arr[1], columnspan=cspan, rowspan=rspan, sticky="w")

    @staticmethod
    def Input(parent, text, var, fs=10, js="left", width=None):
        Widget.Caption(parent, text)
        ttk.Entry(parent, justify=js, textvariable=var, width=width, font=("Inter", fs)
        ).pack()

    @staticmethod
    def InputGrid(parent, text, var, arr, cspan=1, rspan=1, width=None, fs=10, js="left", state="normal", gap=[10, 0]):
        fr = ttk.Frame(parent)
        Widget.CaptionGrid(fr, text, arr, cspan, rspan)
        et = None
        if width:
            et = ttk.Entry(fr, state=state, justify=js, textvariable=var, font=("Inter", fs), width=width)
        else:
            et = ttk.Entry(fr, state=state, justify=js, textvariable=var, font=("Inter", fs))

        et.grid(column=arr[0], row=(arr[1]+1), columnspan=cspan, rowspan=rspan)
        fr.grid(column=arr[0], row=arr[1], padx=gap[0], pady=gap[1])

class MsgBox:
    def PopUp(self, mode, title, msg):
        if mode=="info":
            messagebox.showinfo( 
                parent=self.toplevel,
                title=title, 
                message=msg
            )
        elif mode=="error":
            messagebox.showerror(
                parent=self.toplevel,
                title=title, 
                message=msg
            )
        elif mode=="warning":
            messagebox.showwarning(
                parent=self.toplevel,
                title=title, 
                message=msg
            )

class Form (MsgBox):
    def __init__(self, app, title):
        self.app = app
        self.display = False
        self.main_window = self.app.ventana
        self.toplevel = tk.Toplevel(self.main_window)
        self.toplevel.iconbitmap("assets/favicon.ico")
        self.toplevel.attributes("-topmost", True)
        self.toplevel.title(f"{title} - MeatFlow")
        Widget.MainLabel(self.toplevel, title)
        self.toplevel.withdraw()  # Inicialmente oculto

        self.buttonStyle = ttk.Style()
        self.buttonStyle.configure("TButton", relief="groove", font=("Inter SemiBold", 10), foreground=COLOR1)

        self.toplevel.resizable(False, False)
        self.toplevel.protocol("WM_DELETE_WINDOW", self.hide)
        # self.toplevel.protocol("WM_DELETE_WINDOW", self.handleQuit)

    def show(self):
        self.display = True
        self.toplevel.deiconify()  # Mostrar el formulario

    def hide(self):
        self.app.updateDashboard()
        self.display = False
        self.toplevel.withdraw()  # Mostrar el formulario

    def handleQuit(self):
        self.toplevel.destroy()
        self.main_window.destroy()

class SecForm (MsgBox):
    def __init__(self, form, title):
        self.form = form
        self.display = False
        self.toplevel = tk.Toplevel(self.form.main_window)
        self.toplevel.title(f"{title} - MeatFlow")
        self.toplevel.iconbitmap("assets/favicon.ico")
        self.toplevel.attributes("-topmost", True)
        self.toplevel.attributes("-topmost", True)
        Widget.MainLabel(self.toplevel, title)
        self.toplevel.withdraw()  # Inicialmente oculto

        self.buttonStyle = ttk.Style()
        self.buttonStyle.configure("TButton", relief="groove", font=("Inter SemiBold", 10), foreground=COLOR1)

        self.toplevel.resizable(False, False)
        self.toplevel.protocol("WM_DELETE_WINDOW", self.hide)

    def show(self):
        self.display = True
        self.toplevel.deiconify()  # Mostrar el formulario

    def hide(self):
        self.display = True
        self.toplevel.withdraw()  # Mostrar el formulario

class ChangePasswForm(Form):
    def __init__(self, app):
        super().__init__(app, "Cambiar contraseña")
        self.newPassw = tk.StringVar()

        Widget.SecLabel(self.toplevel, "Ingresa tu nueva contraseña")

        fr = tk.Frame(self.toplevel); fr.pack(pady=(10, 20))

        Widget.Input(fr, "Nueva contraseña:", self.newPassw, js="center")
        
        ttk.Button(fr, text="Cambiar contraseña", width=20, command=self.changePassw).pack(pady=20)

    def changePassw(self):
            if Auth.changePassw(self.app.user["user"], self.newPassw.get()):
                self.hide()

class LoginForm (Form):
    def __init__(self, main_window):
        super().__init__(main_window, "Inicio de Sesión")
        self.user = None

        # Variables de los inputs
        self.userVar = tk.StringVar()
        self.passVar = tk.StringVar()

        # Titulo
        Widget.SecLabel(self.toplevel, "Ingresa con las credenciales provistas")

        # Frame (Usuario)
        fUser = tk.Frame(self.toplevel)
        fUser.pack(pady=10)

        # Frame (Contraseña)
        fPassw = tk.Frame(self.toplevel)
        fPassw.pack(pady=10)

        # Frame (Botones)
        fBtns = tk.Frame(self.toplevel)
        fBtns.pack(pady=(30, 30))

        Widget.Caption(fUser, "Usuario:")
        ttk.Entry(fUser, textvariable=self.userVar, justify="center", font=("Inter", 11)
        ).pack()
        
        Widget.Caption(fPassw, "Contraseña:")
        ttk.Entry(fPassw, textvariable=self.passVar, justify="center", show="*", font=("Inter", 11)
        ).pack()

        # Button (Limpiar)
        ttk.Button(fBtns, text="Limpiar", width=10, command=self.handleClean).grid(column=1, row=0, padx=5)
        # Button (Ingresar)
        ttk.Button(fBtns, text="Ingresar...", width=15, command=self.handleLoginSubmit).grid(column=0, row=0, padx=5)
        self.toplevel.bind("<Return>", self.handleLoginSubmit)

        self.toplevel.protocol("WM_DELETE_WINDOW", self.handleQuit)
        self.show()
        

    def userLogout(self):
        self.user.logout()

    def handleLoginSubmit(self, event=None):
        if self.userVar.get() and self.passVar.get():
            self.user = AuthUser(self.userVar.get())
            try:
                result = self.user.login(self.passVar.get())
                if result:
                    self.app.user["user"] = result["user"]
                    self.app.user["name"].set(result["name"])
                    self.hide()
                    self.main_window.deiconify()
            except Exception as e:
                messagebox.showwarning(
                    parent=self.toplevel,
                    title="Error al iniciar sesión", 
                    message=str(e)
                )

    def handleClean(self):
        self.userVar.set("")
        self.passVar.set("")

class ProductForm (SecForm):
    def __init__(self, main_window):
        super().__init__(main_window, "Productos")
        Widget.SecLabel(self.toplevel, "Añade un nuevo producto")

        self.nameVar = tk.StringVar()
        self.catVar = tk.StringVar()
        self.pr_buyVar = tk.DoubleVar()
        self.pr_sellVar = tk.DoubleVar()
        self.expVar = tk.StringVar()
        self.stockVar = tk.IntVar()
        self.typeVar = tk.StringVar()

        fr1 = tk.Frame(self.toplevel); fr1.pack(pady=5, padx=60)
        fr2 = tk.Frame(self.toplevel); fr2.pack(pady=5)
        fr3 = tk.Frame(self.toplevel); fr3.pack(pady=5)
        fr4 = tk.Frame(self.toplevel); fr4.pack(pady=5)
        fr5 = tk.Frame(self.toplevel); fr5.pack(pady=30)

        Widget.InputGrid(fr1, "Nombre producto:", self.nameVar, [0, 0], width=40)

        # Option Menu (Categoria)
        estilo = ttk.Style()
        estilo.configure("Basic.TMenubutton",
                width=15,
                background="white",
                font=("Inter", 10))

        o_cat = ["Seleccionar", "Carniceria", "Comida", "Producto"]
        fr = tk.Frame(fr2)
        Widget.CaptionGrid(fr, "Categoria:", [0, 0])
        self.catVar.set(o_cat[0])
        ttk.OptionMenu(fr, self.catVar, *o_cat, style="Basic.TMenubutton").grid(column=0, row=1)
        fr.grid(column=0, row=0)

        Widget.InputGrid(fr2, "Tipo:", self.typeVar, [1, 0], width=15)

        Widget.InputGrid(fr3, "Precio Compra:", self.pr_buyVar, [0, 0], width=16)
        Widget.InputGrid(fr3, "Precio Venta:", self.pr_sellVar, [1, 0], width=16)
        Widget.InputGrid(fr4, "Stock:", self.stockVar, [0, 0], width=8)
        Widget.InputGrid(fr4, "Fecha de Vencimiento:", self.expVar, [1, 0], width=20)

        ttk.Button(fr5,text="Añadir",width=20, command=self.addProduct
        ).grid(column=0, row=0)

    def addProduct(self):
        if self.nameVar.get()!="" and self.catVar.get()!="" and self.expVar.get()!="" and self.typeVar.get()!="" and self.pr_buyVar.get()!=0 and self.pr_sellVar.get()!=0 and self.stockVar.get()!=0:
            data = {
                "name": self.nameVar.get(),
                "category": self.catVar.get(),
                "price_buy": self.pr_buyVar.get(),
                "price_sell": self.pr_sellVar.get(),
                "exp_date": self.expVar.get(),
                "stock": self.stockVar.get(),
                "type": self.typeVar.get(),
            }
            try:
                self.form.addProduct(data)
                self.PopUp("info",
                    "Producto agregado!", 
                    "Se agrego correctamente!"
                    )
                self.setDefault()
            except Exception as e:
                self.PopUp("error",
                    "Error en producto!", 
                    "No se completo el registro!"
                )
                print(e)
        else:
            self.PopUp("error",
                "Campos requeridos", 
                "Todos los campos son requeridos"
            )

    def setDefault(self):
        self.nameVar.set("")
        self.catVar.set("")
        self.pr_buyVar.set(0)
        self.pr_sellVar.set(0)
        self.expVar.set("")
        self.stockVar.set(0)
        self.typeVar.set("")

class StockForm (Form):
    def __init__(self, main_window):
        super().__init__(main_window, "Inventario")
        Widget.SecLabel(self.toplevel, "Visualiza el inventario actual")

        self.products = self.loadFromDB()

        def handleFilter():
            resutl = DB.searchBy("productos", "name", self.namefl.get())
            self.setData(resutl)

        #? FILTRO DE BUSQUEDA
        self.namefl = tk.StringVar()

        tk.Label(self.toplevel, text="Filtros").pack()
        ftfr = tk.Frame(self.toplevel)
        tk.Label(ftfr, text="Nombre: ").pack(side="left")
        ttk.Entry(ftfr, textvariable=self.namefl).pack(side="left", padx=10)
        ttk.Button(ftfr, text="Filtrar", command=handleFilter).pack(side="left")
        ftfr.pack(pady=(0, 20))

        #? COMPONENTE DE LISTA INVENTARIO
        w=800
        container = tk.Frame(self.toplevel)
        container.pack(pady=(0, 50))

        canvas = tk.Canvas(container, width=w, height=400)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrolly = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.config(yscrollcommand=scrolly.set)

        self.hd = tk.Frame(canvas)
        canvas.create_window((w/2,0), window=self.hd, anchor="n")

        def update_scroll(event):
            canvas.config(scrollregion=canvas.bbox("all"))

        self.hd.bind("<Configure>", update_scroll)

        self.setData(self.products)

    def loadFromDB(self):
        return DB.get("productos")
    
    def setData(self, data=None):
        self.clearCanvas()
        if data == []:
            data = self.loadFromDB()
            
        gap = 5
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Nombre:").grid(column=0, row=0, padx=gap, sticky="w")
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Categoria:").grid(column=1, row=0, padx=gap)
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Precio Compra:").grid(column=2, row=0, padx=gap)
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Precio Venta:").grid(column=3, row=0, padx=gap)
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Vencimiento:").grid(column=4, row=0, padx=gap)
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Stock:").grid(column=5, row=0, padx=gap)
        tk.Label(self.hd,font=("Inter Semibold", 10), text="Tipo:").grid(column=6, row=0, padx=gap)

        for i, prod in enumerate(data):
            bg = COLOR1_SOFT if i%2==0 else None
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["name"]).grid(column=0, row=(i+1), padx=gap, sticky="w")
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["category"]).grid(column=1, row=(i+1), padx=gap)
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["price_buy"]).grid(column=2, row=(i+1), padx=gap)
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["price_sell"]).grid(column=3, row=(i+1), padx=gap)
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["exp_date"]).grid(column=4, row=(i+1), padx=gap)
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["stock"]).grid(column=5, row=(i+1), padx=gap)
            tk.Label(self.hd,background=bg, font=("Inter", 9), text=prod["type"]).grid(column=6, row=(i+1), padx=gap)
    
    def clearCanvas(self):
        for wg in self.hd.winfo_children():
            wg.destroy()

class BuyForm (Form):
    def __init__(self, form):
        super().__init__(form, "Compra")
        Widget.SecLabel(self.toplevel, "Registra una nueva compra")

        self.productForm = ProductForm(self)
        self.products = []

        fr0 = tk.Frame(self.toplevel); fr0.pack(pady=5)
        fr1 = tk.Frame(self.toplevel); fr1.pack(pady=5, padx=80)
        fr2 = tk.Frame(fr1); fr2.grid(column=0, row=0, padx=10)
        fr3 = tk.Frame(fr1); fr3.grid(column=1, row=0, padx=10)
        footer = tk.Frame(self.toplevel); footer.pack(pady=(20, 40))

        self.nameVar = tk.StringVar()
        self.timeDVar = tk.IntVar()
        self.prodSearch = tk.StringVar()
        self.costoVar = tk.IntVar()

        Widget.InputGrid(fr0, "Nombre proveedor:", self.nameVar, [0,0])
        
        Widget.InputGrid(fr0, "Tiempo de entrega: (dias)", self.timeDVar, [1,0], width=8)

        Widget.CaptionGrid(fr2, "Productos Comprados:", [0, 2])
        self.prodNameList = tk.Listbox(fr2, height=7)

        ttk.Button(fr3, text="Agregar producto", command=self.showProductForm).pack()
        ttk.Button(fr3, text="Eliminar selección", command=self.deleteProduct).pack(pady=(0, 20))

        Widget.Caption(fr3, "Costo Total")
        ttk.Entry(fr3, state="readonly", textvariable=self.costoVar, font=("Inter", 10), width=10).pack()

        ttk.Button(footer, text="Registrar compra", command=self.addBuy, width=20).pack()

        self.prodNameList.grid(column=0, row=3)

    def addProduct(self, data):
        self.products.append(data)
        self.prodNameList.insert(tk.END, data["name"])
        self.updateCostoTotal()
    
    def deleteProduct(self):
        indice = self.prodNameList.curselection()[0]
        del self.products[indice]
        self.prodNameList.delete(indice)
        self.updateCostoTotal()

    def updateCostoTotal(self):
        costo = 0
        for _ in self.products:
            costo += (_["price_buy"] * _["stock"])
        self.costoVar.set(costo)

    def addBuy(self):
        # Datos proveedor
        nameSupp = self.nameVar.get()
        timeDel = self.timeDVar.get()
        
        if nameSupp != "" and timeDel != 0 and len(self.products):
            #? Añadimos al Proveedor
            supplier = Proveedor(nameSupp, self.products, int(timeDel))
            supplier.register()

            #? Añadimos los productos
            for _ in self.products:
                prod = Producto(_)
                prod.register()

            #? Añadimos la compra
            compra = Compra(nameSupp, self.products, costototal=self.costoVar.get())
            compra.register()
            
            self.PopUp(
                "info",
                "Compra realizada",
                "Se añadio una nueva compra"
            )
            self.hide()

        else:
            self.PopUp(
                "warning",
                "Campos requeridos",
                "Añade suficientes datos para procesar la compra"
            )          

    def showProductForm(self):
        self.productForm.show()

class Client(Form):
    def __init__(self, main_window):
        super().__init__(main_window, "Registro Cliente")
        self.name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.id = tk.StringVar()
        self.feedback = tk.StringVar()

        self.sale = Sale(self)

        def validar_cliente(bol):
            result = DB.getOneBy("clientes", "id", self.id.get())
            if result != None and self.id.get() == result["id"]:
                name, last_name = result["name"].split(" ",1)
                self.name.set(name)
                self.last_name.set(last_name)
                self.feedback.set("")
                return False
            else:
                if bol:
                    self.PopUp("info", "Cliente", "Cliente no registrado")
                return True
        
        def registrar():
            if validar_cliente(False):
                if self.id.get() != "" and self.last_name.get() != "" and self.name.get() != "":
                        data = {
                            "id": self.id.get(),
                            "name": f"{self.name.get()} {self.last_name.get()}",
                            "frec_visit": 1,
                            "feedback": self.feedback.get()
                        }
                        cliente = Cliente(data)
                        cliente.register()
                else: 
                    self.PopUp("info", "Cliente", "Debe llenar todos los campos")
            else:
                self.PopUp("info", "Cliente", "Cliente ya registrado")
                
        def showSaleForm():
            if self.id.get() != "" and self.last_name.get() != "" and self.name.get() != "":
                if not validar_cliente(True):
                    self.sale.show()
            else:
                if self.id.get() != "":
                    self.PopUp("info", "Cliente", "Consulte el cliente")
                else:
                    self.PopUp("info", "Cliente", "Ingrese la V- del cliente")
                
        fr1 = tk.Frame(self.toplevel); fr1.pack(pady=10, padx=30)
        fr2 = tk.Frame(self.toplevel); fr2.pack(pady=5)
        fr3 = tk.Frame(self.toplevel); fr3.pack(pady=5)
        fr4 = tk.Frame(self.toplevel); fr4.pack(pady=(20, 5))
        fr5 = tk.Frame(self.toplevel); fr5.pack(pady=(0, 30))
        
        Widget.Caption(fr1, "Cedula Del Cliente: ", "left")
        ttk.Entry(fr1, textvariable=self.id).pack(side="left", padx=6)
        
        ttk.Button(fr1, text="Ver Cliente", command = lambda:validar_cliente(True)).pack(side="left")

        
        Widget.InputGrid(fr2, "Nombre del cliente:", self.name, [0, 0], width=16)
        Widget.InputGrid(fr2, "Apellido del cliente:", self.last_name, [1, 0], width=16)
        
        Widget.CaptionGrid(fr3, "Comentario:", [0, 0])
        entryfeedback = ttk.Entry(fr3, textvariable=self.feedback, font=("Inter", 10),width=30)
        entryfeedback.grid(column=0, row=3, ipady = 10)
        ttk.Button(fr4, text="Añadir Cliente", width=20,command=registrar).grid(column=0, row=0)
        ttk.Button(fr5, text="Ir al carrito", width=20,command=showSaleForm).grid(column=0, row=0)

class Sale(SecForm):
    def __init__(self, main_window):
        super().__init__(main_window, "Orden de Venta")
        self.date = tk.StringVar()
        self.date.set(str(datetime.now().date()))

        self.pay = tk.StringVar()
        self.bill = tk.StringVar()
        self.bill.set(Venta.num_bill())

        # Lista de productos comprados
        self.products_list = []

        # Datos del Cliente
        self.id = self.form.id
        self.name = self.form.name
        self.last_name = self.form.last_name
        
        def registrar_venta():
            if self.pay.get() != "" and self.products_list != []:
                prods = []
                for prod in self.products_list:
                    name = prod.split("x")[0][:-1]
                    amount = prod.split("x")[1]
                    prods.append({
                        "name": name,
                        "amount": int(amount)
                    })

                venta = Venta(
                    self.id.get(),
                    self.pay.get(),
                    prods
                )
                venta.register()

                self.PopUp("info", "Ventas", "Venta registrada")
            else:
                self.PopUp("error", "Error", "Debe llenar todos los campos")
        
        fr1 = tk.Frame(self.toplevel); fr1.pack(pady=10)
        fr2 = tk.Frame(self.toplevel); fr2.pack(pady=5, padx=40)
        
        # Mostrar el cliente
        tk.Label(fr1, text="Cliente:").pack(side="left")
        tk.Label(fr1, textvariable=self.name).pack(side="left", padx=5)
        tk.Label(fr1, textvariable=self.last_name).pack(side="left", padx=5)

        # Campos de entrada
        Widget.InputGrid(fr2, "Fecha:", self.date, [0, 0], width=16, state="readonly", js="center")

        fr = tk.Frame(fr2); fr.grid(column=1, row=0)
        # Widget.Caption(fr2, "Método de pago:", self.pay, [1, 0], width=16)

        Widget.Caption(fr, "Método de pago:")
        op = ["Efectivo", "Tarjeta", "Transferencia"]
        ttk.OptionMenu(fr, self.pay, op[0], *op, style="Basic.TMenubutton").pack()
        Widget.InputGrid(fr2, "N° de Billete:", self.bill, [2, 0], width=16, state="readonly", js="center")
        
        fr3 = tk.Frame(self.toplevel); fr3.pack()

        # Sección de productos
        fr_products = tk.Frame(fr3)
        fr_products.grid(column=0, row=0, pady=5, padx=30)

        queryFrame = tk.Frame(fr_products); queryFrame.grid(column=0, row=1, padx=20, pady=20)
        self.query = tk.StringVar()
        Widget.CaptionGrid(queryFrame, "Producto: ", [0, 0])
        entryQuery = ttk.Entry(queryFrame, textvariable=self.query, width=15)
        entryQuery.grid(column=0, row=1)

        self.quantity = tk.IntVar()
        Widget.CaptionGrid(queryFrame, "Cantidad: ", [1, 0])
        ttk.Entry(queryFrame, textvariable=self.quantity, width=8).grid(column=1, row=1)

        def handleQuery(event=None):
            self.listNameProd.delete(0, tk.END)
            prods = DB.searchBy("productos", "name", entryQuery.get())
            for _ in prods:
                self.listNameProd.insert(tk.END, _["name"])
        
        def handleSelect(event=None):
            i = self.listNameProd.curselection()[0]
            prod = self.listNameProd.get(i)
            self.query.set(prod)

        self.listNameProd = tk.Listbox(queryFrame, height=5)
        self.listNameProd.grid(column=0, row=2, columnspan=3, pady=(5, 10))

        entryQuery.bind("<KeyRelease>", handleQuery)
        self.listNameProd.bind("<<ListboxSelect>>", handleSelect)

        ttk.Button(queryFrame, text="Agregar", command=self.add_product).grid(column=0, row=3, columnspan=3)

        # Caja de texto para mostrar productos agregados
        self.products_display = tk.Text(fr3, height=10, width=40, state="disabled")
        self.products_display.grid(column=1, row=0 )

        # Boton de Facturar
        fr_facturar = tk.Frame(self.toplevel); fr_facturar.pack(pady=25)
        ttk.Button(fr_facturar,text="Facturar",width=20, command=registrar_venta
        ).grid(column=0, row=0)
        
    def add_product(self):
        """Agrega un producto con cantidad a la lista y lo muestra en la caja de texto."""
        product = self.query.get()
        quantity = self.quantity.get()

        prodData = []
        if product and int(quantity) > 0:
            prodData = DB.getOneBy("productos", "name", product)

            if quantity <= prodData["stock"]:
                product_entry = f"{product} x{quantity}"  # Formato "Jamón x2"
                self.products_list.append(product_entry)

                # Mostrar en la caja de texto
                self.products_display.config(state="normal")
                self.products_display.insert(tk.END, f"{product_entry}\n")
                self.products_display.config(state="disabled")

                # Limpiar los campos de entrada
                self.query.set("")
                self.quantity.set(0)
            else:
                self.PopUp("error", "⚠️ Error", "Excedes la cantidad del producto en stock, ingresa una cantidad válida")
        else:
            self.PopUp("error", "⚠️ Error", "Ingresa un producto y una cantidad válida.") 
         
class ReporteForm(Form):
    def __init__(self, main_window):
        super().__init__(main_window, "Reporte de Ventas")
        Widget.SecLabel(self.toplevel, "Visualiza el reporte de ventas y tendencias")

        # Cargar datos usando handledb.DB
        self.reporte = self.cargar_datos_reporte()

        # Filtro de búsqueda
        self.namefl = tk.StringVar()
        tk.Label(self.toplevel, text="Filtros").pack()
        ftfr = tk.Frame(self.toplevel)
        tk.Label(ftfr, text="Producto: ").pack(side="left")
        tk.Entry(ftfr, textvariable=self.namefl).pack(side="left", padx=10)
        tk.Button(ftfr, text="Filtrar", font=("Inter", 9), command=self.handleFilter).pack(side="left")
        ftfr.pack(pady=(0, 20))

        # Contenedor de reportes
        self.report_frame = tk.Frame(self.toplevel)
        self.report_frame.pack(pady=(0, 20))

        # Botón para graficar tendencias
        tk.Button(self.toplevel, text="Graficar Tendencias", command=self.graficar_tendencias).pack()

        # Contenedor del gráfico
        self.graph_frame = tk.Frame(self.toplevel)
        self.graph_frame.pack()

        self.setData()

    def cargar_datos_reporte(self):
        """Carga solo los productos y cantidades vendidos desde la base de datos JSON y crea el objeto Reporte."""

        ventas_data = DB.get("ventas")  # Cargar ventas desde JSON 
        if not ventas_data:
            pass

        # Extraer solo productos y cantidades
        ventas = []
        for data in ventas_data:
            try:
                venta = Venta(
                    fecha=data["fecha"],
                    productos_vendidos=data["productos_vendidos"],
                    metodo_pago=data["metodo_pago"],
                    puntuacion_atencion=data["puntuacion_atencion"]
                )
                ventas.append(venta)
            except KeyError as e:
                pass
        inventario = Inventario()
        inventario.products = DB.get("productos")
        if not inventario.products:
            pass

        return Reporte(inventario, ventas)

    def handleFilter(self):
    
        """Filtra los productos vendidos según el nombre ingresado en la barra de búsqueda."""
        filtro = self.namefl.get().strip().lower()

        if not filtro:
            self.setData(self.reporte.generar_reporte_ventas())
            return

        # Obtener todas las ventas
        ventas_data = DB.get("ventas")
        ventas_filtradas = {}

        print(ventas_data)

        for venta in ventas_data:
            for item in venta["productos"]:
                nombre_producto = item["name"].lower()
                if filtro in nombre_producto:
                    ventas_filtradas[item["name"]] = ventas_filtradas.get(item["name"], 0) + item["amount"]

        self.setData(ventas_filtradas)

    def setData(self, data=None):
        """Muestra el reporte de ventas en la interfaz."""
        for widget in self.report_frame.winfo_children():
            widget.destroy()  # Limpia el frame antes de agregar nuevos datos

        if data is None:
            data = self.reporte.generar_reporte_ventas()

        # Encabezado
        tk.Label(self.report_frame, text="Producto", font=("Inter Semibold", 10)).grid(row=0, column=0)
        tk.Label(self.report_frame, text="Cantidad Vendida", font=("Inter Semibold", 10)).grid(row=0, column=1)

        # Mostrar los productos
        for i, (producto, cantidad) in enumerate(data.items()):
            bg = COLOR1_SOFT if i%2==0 else None
            tk.Label(self.report_frame,background=bg, text=producto, font=("Inter", 9)).grid(row=i + 1, column=0)
            tk.Label(self.report_frame,background=bg, text=str(cantidad), font=("Inter", 9)).grid(row=i + 1, column=1)


    def graficar_tendencias(self):
        """Genera y muestra un gráfico de tendencias dentro de Tkinter."""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4))
        tendencias = self.reporte.graficar_tendencias()

        for producto, valores in tendencias.items():
            ax.plot(valores['fechas'], valores['cantidades'], label=producto)

        ax.set_xlabel('Fecha')
        ax.set_ylabel('Cantidad Vendida')
        ax.set_title('Tendencias de Ventas')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()