# cambio_escenarios.py
import pygame

class Teletransporte:
    def __init__(self, cambios=None):
        self.cambios = cambios or []
        self.cooldown = 0

    def deteccion(self, jugador, obstaculos, delta_time):
        # Deshabilitado para la Beta (no hacer nada)
        return None

class ZonaTeleport:
    def __init__(self, x=0, y=0, width=0, height=0, destino=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.destino = destino
