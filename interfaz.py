from tkinter import *
from tkinter import ttk
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


class MainWindow(Tk, CentrarVentanaMixin):
    def __init__(self):
        super().__init__() #Llamo al constructor de la clase heredada(Tk)
        self.title("Gestor de clientes")
        self.build()
        self.centrar_ventana()

    def build(self):
        marco = Frame(self)#Hereda de self porque tiene que insertarlo en la propia "MainWindow"
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

        frame = Frame(self)
        frame.pack(pady=20)

        Button(frame, padx=20, bd=5, text="Crear", command=None).grid(row=0, column=0)
        Button(frame, padx=20, bd=5, text="Modificar", command=None).grid(row=0, column=1)
        Button(frame, padx=20, bd=5, text="Borrar", command=None).grid(row=0, column=2)

        self.treeview = treeview #Para poder tener acceso a el en los demas métodos


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()