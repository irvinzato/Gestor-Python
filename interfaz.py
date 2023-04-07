from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
import database as db
import helpers

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


                        #"Toplevel" maneja las sub ventanas de "TK", automáticamente la Sub ventana sabe quien es su padre
class VentanaCrearCliente(Toplevel, CentrarVentanaMixin):
    def __init__(self, padre):
        super().__init__(padre) #Llamo al constructor de la clase heredada
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
        ine.bind("<KeyRelease>", lambda evento: self.validar(evento, 0)) #Configuración del evento, para poder pasarle parámetros se ocupa usar función anonima(lambda)

        nombre = Entry(marco)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda evento: self.validar(evento, 1))

        apellido = Entry(marco)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda evento: self.validar(evento, 2))

        marco_2 = Frame(self)
        marco_2.pack(pady=10)

        crear = Button(marco_2, text="Crear", command=self.crear_cliente)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(marco_2, text="Cancelar", command=self.cerrar).grid(row=0, column=1)

        self.validaciones = [0, 0, 0] #Tendre un [True, True, True] si todo esta validado correctamente
        
        #Exporto las variables para poder usarlas en otros métodos de la clase
        self.crear    = crear            #Asigno el valor del botón(crear) para poder usarlo en las validaciones
        self.ine      = ine
        self.nombre   = nombre
        self.apellido = apellido

    def crear_cliente(self):
        #"master" es el padre de la sub ventana(ventana principal)
        self.master.treeview.insert(
                parent='', index='end', iid=self.ine.get(),  #Con ".get()" porque son campos de texto(Entrys)
                values=(self.ine.get(), self.nombre.get(), self.apellido.get())
            )
        db.Clientes.crear(self.ine.get(), self.nombre.get(), self.apellido.get())
        self.cerrar()

    def validar(self, evento, indice):
        """ ¡ Todo este código lo refactorice abajo con operadores ternarios !
        valor = evento.widget.get() #Recupero lo que tiene el campo de la ventana
        if indice == 0:
            valido = helpers.ine_valido(valor, db.Clientes.lista)
            if valido:
                evento.widget.configure({"bg": "Green"})
            else:
                evento.widget.configure({"bg": "Red"})
        if indice == 1:
            #"isalpha()" es una función que retorna True si la cadena recuperada es alfabetica(Tambien podria hacer mi propia función para validar, como el ine)
            valido = valor.isalpha() and len(valor) >= 2 and len(valor) <= 30
            if valido:
                evento.widget.configure({"bg": "Green"})
            else:
                evento.widget.configure({"bg": "Red"})
        if indice == 2:
            valido = valor.isalpha() and len(valor) >= 2 and len(valor) <= 30
            if valido:
                evento.widget.configure({"bg": "Green"})
            else:
                evento.widget.configure({"bg": "Red"})
        """
        """ valor = evento.widget.get() #Recupero lo que tiene el campo de la ventana
        if indice == 0:
            evento.widget.configure({"bg": "Green"}) if helpers.ine_valido(valor, db.Clientes.lista) else evento.widget.configure({"bg": "Red"})
        if indice == 1:
            evento.widget.configure({"bg": "Green"}) if valor.isalpha() and len(valor) >= 2 and len(valor) <= 30 else evento.widget.configure({"bg": "Red"})
        if indice == 2:
            evento.widget.configure({"bg": "Green"}) if valor.isalpha() and len(valor) >= 2 and len(valor) <= 30 else evento.widget.configure({"bg": "Red"})
        """
        """ ¡ Mi solución anterior la puedo reducir aun más ! """
        ## La mejor solución de las dos anteriores ##
        valor = evento.widget.get() #Recupero lo que tiene el campo de la ventana
        valido = helpers.ine_valido(valor, db.Clientes.lista) if indice == 0 else valor.isalpha() and len(valor) >= 2 and len(valor) <= 30
        evento.widget.configure({"bg": "Green" if valido else "Red"})
        ### Cambiare el estado del botón en base a las validaciones ###
        self.validaciones[indice] = valido
        self.crear.config(state=NORMAL if self.validaciones == [True, True, True] else DISABLED)  #Cambio estado del botón

    ### Para cerrar un "Toplevel" ###
    def cerrar(self):
        self.destroy()
        self.update()


class VentanaEditarCliente(Toplevel, CentrarVentanaMixin):
    def __init__(self, padre):
        super().__init__(padre) 
        self.title("Actualizar cliente")
        self.build()
        self.centrar_ventana()
        #Para impedir hacer acción en la otra ventana si tenemos esta abierta "transient" y "grab_set"
        self.transient(padre)
        self.grab_set()

    def build(self):
        marco = Frame(self) #Aquí si pide el self, para que el frame lo ponga dentro de "VentanaCrearCliente"
        marco.pack(padx=20, pady=10)

        Label(marco, text="INE (NO EDITABLE)").grid(row=0, column=0)
        Label(marco, text="Nombre (2 a 30 carácteres)").grid(row=0, column=1)
        Label(marco, text="Apellido (2 a 30 carácteres)").grid(row=0, column=2)

        ine = Entry(marco)
        ine.grid(row=1, column=0)

        nombre = Entry(marco)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda evento: self.validar(evento, 0))

        apellido = Entry(marco)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda evento: self.validar(evento, 1))

        ### Recupero los valores donde esta el foco(de la ventana principal) y los agrego en los campos Entry ###
        cliente = self.master.treeview.focus()
        campos  = self.master.treeview.item(cliente, 'values')
        
        ine.insert(0, campos[0])  #Añado en la primera posicion del campo el valor recuperado del "master"
        ine.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])


        marco_2 = Frame(self)
        marco_2.pack(pady=10)

        actualizar = Button(marco_2, text="Actualizar", command=self.editar_cliente)
        actualizar.grid(row=0, column=0)
        Button(marco_2, text="Cancelar", command=self.cerrar).grid(row=0, column=1)

        self.validaciones = [1, 1] #[True, True] por defecto porque cargo los valores con algo que ya esta validado
        
        self.actualizar = actualizar
        self.ine        = ine
        self.nombre     = nombre
        self.apellido   = apellido

    def editar_cliente(self):
        cliente = self.master.treeview.focus()
        self.master.treeview.item(cliente, values=(self.ine.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.ine.get(), self.nombre.get(), self.apellido.get())
        self.cerrar()

    def validar(self, evento, indice):
        valor  = evento.widget.get() #Recupero lo que tiene el campo de la ventana
        valido = valor.isalpha() and len(valor) >= 2 and len(valor) <= 30
        evento.widget.configure({"bg": "Green" if valido else "Red"})
        ### Cambiare el estado del botón en base a las validaciones ###
        self.validaciones[indice] = valido
        self.actualizar.config(state=NORMAL if self.validaciones == [True, True] else DISABLED)  #Cambio estado del botón

    def cerrar(self):
        self.destroy()
        self.update()

### CLASE PRINCIPAL ###
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

        Button(marco_2, padx=20, bd=5, text="Crear",     command=self.crear).grid(row=0, column=0)
        Button(marco_2, padx=20, bd=5, text="Modificar", command=self.editar).grid(row=0, column=1)
        Button(marco_2, padx=20, bd=5, text="Borrar",    command=self.borrar).grid(row=0, column=2) #Al llamar el metodo aqui no se usa con "()"

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
                db.Clientes.borrar(campos[0])

    def crear(self):
        VentanaCrearCliente(self)

    def editar(self):
        if self.treeview.focus():
            VentanaEditarCliente(self)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()