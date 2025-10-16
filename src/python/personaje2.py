# personaje2.py
import pygame
from compilados_py.Release import personaje as per

class Protagonista(per.Personaje):
    def __init__(self, movimiento, dinero, animaciones, eje_x, eje_y, velocidad, inventario=None):
        super().__init__(movimiento, dinero)
        self.eje_x = eje_x
        self.eje_y = eje_y
        self.velocidad = velocidad
        self.base_vel = velocidad
        self.flip_x = False
        self.flip_y = False
        self.inventario = inventario
        self.estados = {
            "alimentacion": 100,
            "recreacion": 100,
            "aceptacion_social": 100,
        }
        self.flags = {}
        self.minimalista = False

        self.rect = pygame.Rect(eje_x, eje_y, 80, 120)
        self.animaciones = animaciones
        self.frame_index = 0
        self.animation_speed = 0.1
        self.current_animation = "idle"
        self.last_update = pygame.time.get_ticks()
        self.animation_states = {
            "idle":[0], "up":[1], "down":[4], "left":[5,6], "right":[5,6]
        }

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 1000:
            self.frame_index += 1
            self.last_update = current_time
            if self.frame_index >= len(self.animation_states.get(self.current_animation,[0])):
                self.frame_index = 0

    def set_animation(self, name):
        if name != self.current_animation:
            self.current_animation = name
            self.frame_index = 0

    def get_current_frame(self):
        frames = self.animation_states.get(self.current_animation, [0])
        idx = self.frame_index % len(frames)
        return self.animaciones[frames[idx]]

    def movimiento(self, obstaculos=None):
        teclas = pygame.key.get_pressed()
        current = "idle"
        old_x, old_y = self.eje_x, self.eje_y

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            self.eje_y -= self.velocidad; current="up"
        elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            self.eje_y += self.velocidad; current="down"
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.eje_x -= self.velocidad; self.flip_x=True; current="left"
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.eje_x += self.velocidad; self.flip_x=False; current="right"

        self.rect.x = int(self.eje_x)
        self.rect.y = int(self.eje_y)

        if obstaculos:
            for o in obstaculos:
                if self.rect.colliderect(o):
                    self.eje_x, self.eje_y = old_x, old_y
                    self.rect.x = int(self.eje_x); self.rect.y = int(self.eje_y)
                    break

        self.set_animation(current)
        self.update_animation()

    def cambio_necesidades(self):
        for k in ("alimentacion","recreacion"):
            if k in self.estados:
                self.estados[k] = max(0, self.estados[k] - 1)

    def abribr_inventario(self, inventario, surface, interfaz):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            inventario.abrir_inventario(surface, interfaz)

    def dibujar(self, surface, camara):
        frame = self.get_current_frame()
        if self.current_animation == "left":
            img = pygame.transform.flip(frame, True, self.flip_y)
        else:
            img = pygame.transform.flip(frame, self.flip_x, self.flip_y)
        surface.blit(img, (self.rect.x - camara.x, self.rect.y - camara.y))

    # utilidades
    def has_item(self, name):
        if not self.inventario: return False
        for it in self.inventario.contenido:
            if getattr(it,"name",None) == name:
                return True
        return False

    def add_flag(self, k, v=True):
        self.flags[k] = v

    def remove_flag(self, k):
        if k in self.flags: del self.flags[k]
