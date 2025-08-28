import pygame

class Personajes ():
    def __init__ (self, eje_x, eje_y, velocidad, ancho, alto):
        self.eje_x = eje_x
        self.eje_y = eje_y
        self.velocidad = velocidad
        self.ancho = ancho
        self.alto = alto

class Jugador (Personajes):
    def __init__(self, eje_x, eje_y, velocidad, ancho, alto):
        super().__init__(eje_x, eje_y, velocidad, ancho , alto)


    def movimiento_jugador (self):
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_w]:
            self.eje_y -= self.velocidad
        if tecla[pygame.K_s]:
            self.eje_y += self.velocidad
        if tecla[pygame.K_a]:
            self.eje_x -= self.velocidad
        if tecla[pygame.K_d]:
            self.eje_x += self.velocidad

    def interaccion (self):
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_e]:
            pass #Aún me falta aprender como hacer eso ...

