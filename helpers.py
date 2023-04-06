import os
import platform
import re

def limpiar_consola():
    #Ternario en Python
    os.system('cls') if platform.system() == "Windows" else os.system('clear')

def leer_texto(longitud_min=2, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input(">")
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto
        else:
            print("Tu texto no cumple con las validaciones de longitud para el campo")

#También valida que el ine no se repita con el de otro cliente
def ine_valido(ine, lista):
    if not re.match('[0-9]{2}[A-Z]$', ine):
        print("INE Incorrecto, debe cumplir el formato")
        return False
    for cliente in lista:
        if cliente.ine == ine:
            print("INE utilizada por otro cliente.")
            return False
    return True

def validar_campo(patron, texto):
    return re.match(patron, texto)