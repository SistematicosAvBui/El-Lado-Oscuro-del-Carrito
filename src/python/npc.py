import pygame
from compilados_py.Release import personaje as per

class NPC (per.Personaje):
    #clase que crea un NPC
    def __init__ (self, movimiento, dinero, eje_x, eje_y, dialogos, sprite):
        super().__init__(movimiento, dinero)
        self.eje_x = eje_x
        self.eje_y = eje_y
        self.dialogos = dialogos
        self.sprite = sprite
        self.rect = self.sprite.get_rect(topleft = (eje_x, eje_y))

    def dialogo (self, dialogo, entrada, personaje):
        if (entrada[pygame.K_e]) and (self.rect.colliderect(personaje.rect)):
            pass

    def dibujar (self, surface):
        surface.blit(self.sprite, self.rect)
