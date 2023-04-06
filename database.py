class Cliente:
    def __init__(self, ine, nombre, apellido):
        self.ine      = ine
        self.nombre   = nombre
        self.apellido = apellido

    def __str__(self):
        return f"({self.ine}) {self.nombre} {self.apellido}"
    
import csv
import config #Para poder separar el programa con las pruebas unitarias

class Clientes:
    lista = []
    #Para implementar persistencia(Todo quedara dentro del csv)
    with open(config.DATABASE_PATH, newline='\n') as fichero:
        reader = csv.reader(fichero, delimiter=';')
        for ine, nombre, apellido in reader:
            cliente = Cliente(ine, nombre, apellido)
            lista.append(cliente)

    @staticmethod
    def buscar(ine):
        for cliente in Clientes.lista:
            if cliente.ine == ine:
                return cliente
            
    @staticmethod
    def crear(ine, nombre, apellido):
        cliente = Cliente(ine, nombre, apellido)
        Clientes.lista.append(cliente)
        Clientes.guardar_en_csv()
        return cliente

    @staticmethod
    def modificar(ine, nombre, apellido):
        for indice,cliente in enumerate(Clientes.lista):
            if cliente.ine == ine:
                Clientes.lista[indice].nombre   = nombre
                Clientes.lista[indice].apellido = apellido
                Clientes.guardar_en_csv()
                return Clientes.lista[indice]

    @staticmethod
    def borrar(ine):
        for indice,cliente in enumerate(Clientes.lista):
            if cliente.ine == ine:
                cliente_recuperado = Clientes.lista.pop(indice)
                Clientes.guardar_en_csv()
                return cliente_recuperado

    @staticmethod        
    def guardar_en_csv():
        with open(config.DATABASE_PATH, 'w', newline='\n') as fichero:
            writer = csv.writer(fichero, delimiter=';')
            for cliente in Clientes.lista:
                writer.writerow((cliente.ine, cliente.nombre, cliente.apellido)) #writerow recibe una tupla