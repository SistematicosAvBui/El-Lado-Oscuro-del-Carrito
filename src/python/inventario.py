import pygame
import ui

interfaz = ui.UI()

class Inventario ():
    def __init__ (self, capacidad):
        self.contenido = []
        self.capacidad = capacidad

    def abrir_inventario (self, jugador, pantalla):
         interfaz.interfaz_inventario (jugador, pantalla)

    def agregar_objeto (self, producto: object):
        if self.capacidad <= 0:
            print("No se puede agregar el objeto al inventario")
        else:
            self.contenido.append(producto)

    def vender_objeto (self, producto: object):
        self.contenido.remove(producto)
