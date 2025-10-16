# inventario.py
import pygame

class Inventario:
    def __init__(self, capacidad):
        # capacidad = espacios libres
        self.contenido = []  # lista de Item (objetos)
        self.capacidad = capacidad

    def abrir_inventario(self, pantalla, interfaz):
        # compatibilidad: interfaz tiene draw_inventory
        return interfaz.interfaz_inventario(pantalla, self.capacidad)

    def agregar_objeto(self, producto):
        if self.capacidad <= 0:
            # no hay espacio
            return False
        self.contenido.append(producto)
        self.capacidad -= 1
        return True

    def vender_objeto(self, index):
        if 0 <= index < len(self.contenido):
            p = self.contenido.pop(index)
            self.capacidad += 1
            return p
        return None

    def usar_objeto(self, index):
        if 0 <= index < len(self.contenido):
            p = self.contenido.pop(index)
            self.capacidad += 1
            return p
        return None

