import pygame
from compilados_py.Release import personaje as per

def definir_animaciones (indice_comienzo, indice_fin, iterable, actualizable):
    cooldown = 500
    for frame in range(indice_comienzo, indice_fin):
        actualizable = iterable[frame]
        if frame == indice_fin:
            frame = indice_comienzo

        

class Protagonista (per.Personaje):
    #Clase que se encarga de generar el personaje jugable:
    #Recibe movimiento, dinero, imagen de Sprite, posicion en X y Y, Velocidad
    def __init__ (self, movimiento, dinero, animacion, eje_x, eje_y, velocidad):
        super().__init__(movimiento, dinero)
        self.eje_x = eje_x
        self.eje_y = eje_y
        self.animacion = animacion[self.frame_index]
        self.conjunto_animaciones = animacion
        self.velocidad = velocidad
        self.forma = pygame.Rect(0, 0, 150, 175)
        self.flip_x = False
        self.flip_y = False
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def movimiento (self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            self.eje_y -= self.velocidad
            definir_animaciones(1, 2, self.conjunto_animaciones, self.frame_index)

        if teclas[pygame.K_s]:
            self.eje_y += self.velocidad
        if teclas[pygame.K_a]:
            self.eje_x -= self.velocidad
            self.flip_x = False
        if teclas[pygame.K_d]:
            self.eje_x += self.velocidad
            self.flip_x = True
    
            

    def dibujar (self, interfaz):
        imagen_flip = pygame.transform.flip(self.animacion, self.flip_x, self.flip_y)
        interfaz.blit(imagen_flip, (self.eje_x, self.eje_y))
