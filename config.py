import sys

DATABASE_PATH = "clientes.csv"

#Para que cuando corra las pruebas unitarias cargue OTRO archivo csv y no modifique el original
if "pytest" in sys.argv[0]:
    DATABASE_PATH = "tests/clientes_test.csv"