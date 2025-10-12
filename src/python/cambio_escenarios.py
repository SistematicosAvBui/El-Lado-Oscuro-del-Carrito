import pygame

class Teletransporte:
    def __init__(self, cambios: list):
        """
        cambios: lista de objetos con atributo .rect y .destino (ruta del fondo)
        """
        self.cambios = cambios
        self.cooldown = 0  # en milisegundos

    def deteccion(self, jugador: object, obstaculos: list, delta_time):
        nuevo_fondo = None

        # Disminuir cooldown si está activo
        if self.cooldown > 0:
            self.cooldown -= delta_time
            return None

        for tp in self.cambios:
            if tp.rect.colliderect(jugador.rect):
                # Cambiar fondo y limpiar obstáculos
                nuevo_fondo = pygame.image.load(tp.destino).convert_alpha()
                obstaculos.clear()

                # Activar cooldown de 1 segundo
                self.cooldown = 1000
                break

        return nuevo_fondo
    


class ZonaTeleport ():
    def __init__ (self, x, y, width, height, destino):
        self.rect = pygame.Rect(x, y, width, height)
        self.destino = destino

