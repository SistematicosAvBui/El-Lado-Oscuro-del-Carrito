# colisiones.py
import pygame

class SistemaColisiones:
    def __init__(self, hitboxes=None):
        self.hitboxes = hitboxes or []
        self.debug_mode = False

    def set_hitboxes(self, hitboxes):
        self.hitboxes = hitboxes or []

    def add_hitbox(self, rect):
        self.hitboxes.append(rect)

    def verificar_colision_rectangulos(self, rect1, rect2):
        return rect1.colliderect(rect2)

    def verificar_colision_multiple(self, rect, lista_rects):
        col = []
        for r in lista_rects:
            if rect.colliderect(r):
                col.append(r)
        return col

    def prevenir_movimiento(self, rect_actual, dx, dy):
        nuevo = rect_actual.copy()
        if dx != 0:
            prueba_x = nuevo.copy()
            prueba_x.x += dx
            if not self.verificar_colision_multiple(prueba_x, self.hitboxes):
                nuevo.x += dx
        if dy != 0:
            prueba_y = nuevo.copy()
            prueba_y.y += dy
            if not self.verificar_colision_multiple(prueba_y, self.hitboxes):
                nuevo.y += dy
        return nuevo

    def dibujar_debug(self, screen, camara, color=(255, 0, 0), grosor=2):
        if not self.debug_mode:
            return
        for r in self.hitboxes:
            draw_rect = pygame.Rect(r.x - camara.x, r.y - camara.y, r.width, r.height)
            pygame.draw.rect(screen, color, draw_rect, grosor)

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode
