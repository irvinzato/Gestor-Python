import unittest
import database as db
import copy

#Utilice el paquete "pytest" para utilizar las pruebas "pytest -v" comprueba en el directorio de pruebas los tests
class TestDataBase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [ db.Cliente("27S", "Irving", "Rivera"), db.Cliente("52L", "Angeles", "Lopez"),
                              db.Cliente("34R", "Jesus" , "Rivera"), db.Cliente("47W", "Laura"  , "Lopez") ]
        
    def test_buscar_cliente(self):
        cliente_existente   = db.Clientes.buscar("27S")
        cliente_inexistente = db.Clientes.buscar("69S")
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)

    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear("25V", "Vladimir", "Macedo")
        self.assertIsNotNone(nuevo_cliente)
        self.assertEqual(len(db.Clientes.lista), 5)
        self.assertEqual(nuevo_cliente.nombre, "Vladimir")

    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar("47W"))
        cliente_modificado  = db.Clientes.modificar("47W", "Elena", "Lopez")
        self.assertIsNotNone(cliente_modificado)
        self.assertEqual(cliente_a_modificar.nombre, "Laura")
        self.assertEqual(cliente_modificado.nombre, "Elena")

    def test_eliminar_cliente(self):
        cliente_eliminado = db.Clientes.borrar("27S")
        buscar_cliente    = db.Clientes.buscar("27S")
        self.assertIsNotNone(cliente_eliminado)
        self.assertIsNone(buscar_cliente)