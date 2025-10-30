import pygame



class Inventario ():
    def __init__ (self, capacidad):
        self.contenido = []
        self.capacidad = capacidad

    def abrir_inventario (self, pantalla, interfaz):
        interfaz.interfaz_inventario (pantalla, interfaz, self.capacidad)

    def agregar_objeto (self, producto: object):
        if self.capacidad <= 0:
            print("No se puede agregar el objeto al inventario")
        else:
            self.contenido.append(producto)
            self.capacidad -= 1

    def vender_objeto (self, producto: object):
        self.contenido.remove(producto)
        self.capacidad += 1



