class Cliente:
    def __init__(self, ine, nombre, apellido):
        self.ine      = ine
        self.nombre   = nombre
        self.apellido = apellido

    def __str__(self):
        return f"({self.ine}) {self.nombre} {self.apellido}"
    
class Clientes:
    lista = []

    @staticmethod
    def buscar(ine):
        for cliente in Clientes.lista:
            if cliente.ine == ine:
                return cliente
            
    @staticmethod
    def crear(ine, nombre, apellido):
        cliente = Cliente(ine, nombre, apellido)
        Clientes.lista.append(cliente)
        return cliente

    @staticmethod
    def modificar(ine, nombre, apellido):
        for indice,cliente in enumerate(Clientes.lista):
            if cliente.ine == ine:
                Clientes.lista[indice].nombre   = nombre
                Clientes.lista[indice].apellido = apellido 
                return Clientes.lista[indice]

    @staticmethod
    def borrar(ine):
        for indice,cliente in enumerate(Clientes.lista):
            if cliente.ine == ine:
                return Clientes.lista.pop(indice)