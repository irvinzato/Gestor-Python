from tkinter import *

class MainWindow(Tk):
    def __init__(self):
        super().__init__() #Llamo al constructor de la clase heredada(Tk)
        self.title("Gestor de clientes")
        self.build()

    def build(self):
        button = Button(self, text="Hola Irving", command=self.hola)
        button.pack()

    def hola(self):
        print("Hola Irving")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()