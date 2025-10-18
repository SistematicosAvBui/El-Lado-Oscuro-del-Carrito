import pygame
from random import randint

class Animal ():
    #Definimos la clase animal para poder generarlos en el mundo
    def __init__ (self, pos_x, pos_y, velocidad, sprite, cantidad):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocidad = velocidad
        self.sprite = sprite
        self.cantidad = cantidad

    def movimiento (self):
        pass