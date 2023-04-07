from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
import database as db

#Un mixin es una clase que contiene una o varias definiciones y podemos heredarlas en otras clases
class CentrarVentanaMixin:
    def centrar_ventana(self):
        self.update()
        w  = self.winfo_width()
        h  = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x  = int(ws/2 - w/2)
        y  = int(hs/2 - h/2) #Altura de la pantalla entre 2 menos altura de la ventana entre 2
        self.geometry(f"{w}x{h}+{x}+{y}") #WIDTHxHEIGHT+OFFSET_X+OFFSET_Y


class VentanaCrearCliente(Toplevel, CentrarVentanaMixin):
    def __init__(self, padre):
        super().__init__(padre) #Llamo al constructor de la clase heredada(Toplevel)
        self.title("Crear cliente")
        self.build()
        self.centrar_ventana()
        #Para impedir hacer acción en la otra ventana si tenemos esta abierta "transient" y "grab_set"
        self.transient(padre)
        self.grab_set()

    def build(self):
        marco = Frame(self) #Aquí si pide el self, para que el frame lo ponga dentro de "VentanaCrearCliente"
        marco.pack(padx=20, pady=10)

        Label(marco, text="INE (2 enteros y 1 upper char)").grid(row=0, column=0)
        Label(marco, text="Nombre (2 a 30 carácteres)").grid(row=0, column=1)
        Label(marco, text="Apellido (2 a 30 carácteres)").grid(row=0, column=2)

        ine = Entry(marco)
        ine.grid(row=1, column=0)
        nombre = Entry(marco)
        nombre.grid(row=1, column=1)
        apellido = Entry(marco)
        apellido.grid(row=1, column=2)

        marco_2 = Frame(self)
        marco_2.pack(pady=10)

        crear = Button(marco_2, text="Crear", command=self.crear_cliente)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(marco_2, text="Cancelar", command=self.cerrar).grid(row=0, column=1)

    def crear_cliente(self):
        pass

    ### Para cerrar un "Toplevel" ###
    def cerrar(self):
        self.destroy()
        self.update()

class MainWindow(Tk, CentrarVentanaMixin):
    def __init__(self):
        super().__init__() #Llamo al constructor de la clase heredada(Tk)
        self.title("Gestor de clientes")
        self.build()
        self.centrar_ventana()

    def build(self):
                #Curiosamente tambien trabaja aunque Frame() no tenga dentro "self"
        marco = Frame(self) #Hereda de self porque tiene que insertarlo en la propia "MainWindow"
        marco.pack()

        treeview = ttk.Treeview(marco)
        treeview['columns'] = ('INE', 'Nombre', 'Apellido') #Ademas de estas columnas crea una extra al inicio

        treeview.column("#0", width=0, stretch=NO) #Configuración de la columna extra que pone por defecto
        treeview.column("INE", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)
        
        #Cabeceras
        treeview.heading("INE", text="INE", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)

        scrollbar = Scrollbar(marco)
        scrollbar.pack(side=RIGHT, fill=Y) #Scroll verticalmente(eje Y)
        treeview['yscrollcommand'] = scrollbar.set

        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='', index='end', iid=cliente.ine,
                values=(cliente.ine, cliente.nombre, cliente.apellido)
            )

        treeview.pack()

        marco_2 = Frame(self)
        marco_2.pack(pady=20)

        Button(marco_2, padx=20, bd=5, text="Crear", command=self.crear).grid(row=0, column=0)
        Button(marco_2, padx=20, bd=5, text="Modificar", command=None).grid(row=0, column=1)
        Button(marco_2, padx=20, bd=5, text="Borrar", command=self.borrar).grid(row=0, column=2) #Al llamar el metodo aqui no se usa con "()"

        self.treeview = treeview #Para poder tener acceso a el en los demas métodos

    def borrar(self):
        cliente = self.treeview.focus() #focus regresa donde tenemos el "foco" en el "treeview"
        if cliente:
            campos = self.treeview.item(cliente, "values") #Extraera los valores del cliente seleccionado en el treeview
            confirmar = askokcancel(
                title="Confirmar borrado",
                message=f"¿Borrar {campos[1]} {campos[2]}?", #Recupere los valores del cliente en una lista
                icon=WARNING
            )
            if confirmar:
                self.treeview.delete(cliente)

    def crear(self):
        VentanaCrearCliente(self)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()