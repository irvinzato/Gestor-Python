import helpers
import database as db

def iniciar():
    while True:
        helpers.limpiar_consola()

        print("======================")
        print(" Bienvenido al Gestor ")
        print("======================")
        print("[1] Listar los clientes")
        print("[2] Buscar cliente")
        print("[3] Añadir cliente")
        print("[4] Modificar cliente")
        print("[5] Eliminar cliente")
        print("[6] Cerrar el Gestor")
        print("======================")

        opcion = input("> ")
        helpers.limpiar_consola()

        if opcion == "1":
            print("Listando los clientes... \n")
            for cliente in db.Clientes.lista:
                print(cliente)

        elif opcion == "2":
            print("Buscando un cliente... \n")
            ine     = helpers.leer_texto(3, 3, "INE(2 int y 1 char)").upper()
            cliente = db.Clientes.buscar(ine)
            print(cliente) if cliente else print("No se encontro el cliente con INE", ine)

        elif opcion == "3":
            print("Añadiendo un cliente... \n")

            ine = None #Por buena práctica ya que lo inicializo dentro del bucle
            while True:
                ine = helpers.leer_texto(3, 3 , "INE(2 int y 1 char)").upper()
                if helpers.ine_valido(ine, db.Clientes.lista):
                    break

            print("INE correcto.")
            nombre   = helpers.leer_texto(2, 30, "Nombre de la persona(De 2 a 30 caracteres)").capitalize()
            apellido = helpers.leer_texto(2, 30, "Apellido de la persona(De 2 a 30 caracteres)").capitalize()
            db.Clientes.crear(ine, nombre, apellido)
            print("Cliente añadido con exito !")

        elif opcion == "4":
            print("Modificando un cliente... \n")
            ine      = helpers.leer_texto(3, 3 , "INE(2 int y 1 char)").upper()
            cliente  = db.Clientes.buscar(ine)
            if cliente:
                nombre   = helpers.leer_texto(2, 30, f"Nombre de la persona [{cliente.nombre}] (De 2 a 30 caracteres)").capitalize()
                apellido = helpers.leer_texto(2, 30, f"Apellido de la persona [{cliente.apellido}] (De 2 a 30 caracteres)").capitalize()
                db.Clientes.modificar(cliente.ine, nombre, apellido)
                print("Cliente modificado correctamente !")
            else:
                print("No se encuentra el cliente con ine", ine)

        elif opcion == "5":
            print("Eliminando un cliente... \n")
            ine = helpers.leer_texto(3, 3 , "INE(2 int y 1 char)").upper()
            print("Cliente eliminado con exito !") if db.Clientes.borrar(ine) else print("No se encontro ningun cliente con ine", ine)

        elif opcion == "6":
            print("Saliendo del Gestor... \n")
            break

        input("\nPresiona ENTER para continuar...")