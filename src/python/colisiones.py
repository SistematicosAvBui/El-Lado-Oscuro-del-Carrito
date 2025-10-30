import pygame

class SistemaColisiones:
    """
    Sistema de colisiones simple y práctico para la beta.
    Mantiene una lista de hitboxes (pygame.Rect en coordenadas del mundo)
    y ofrece métodos para prevenir movimiento y dibujar debug (offset cámara).
    """

    def __init__(self, hitboxes=None):
        # hitboxes: lista de pygame.Rect
        self.hitboxes = hitboxes or []
        self.debug_mode = False

    def set_hitboxes(self, hitboxes):
        self.hitboxes = hitboxes or []

    def add_hitbox(self, rect):
        self.hitboxes.append(rect)

    def verificar_colision_rectangulos(self, rect1, rect2):
        """True si rect1 colisiona con rect2."""
        return rect1.colliderect(rect2)

    def verificar_colision_multiple(self, rect, lista_rects):
        """Devuelve la lista de rects de lista_rects que colisionan con rect."""
        col = []
        for r in lista_rects:
            if rect.colliderect(r):
                col.append(r)
        return col

    def prevenir_movimiento(self, rect_actual, dx, dy):
        """
        Intenta mover rect_actual por (dx, dy), pero previene la penetración.
        Hacemos resolución por ejes: primero X (si es posible), luego Y.
        Devuelve un nuevo pygame.Rect (no modifica el original).
        """
        nuevo = rect_actual.copy()

        # Probar movimiento en X
        if dx != 0:
            prueba_x = nuevo.copy()
            prueba_x.x += dx
            if not self.verificar_colision_multiple(prueba_x, self.hitboxes):
                nuevo.x += dx
            else:
                # no mover en X (se evita penetración)
                pass

        # Probar movimiento en Y
        if dy != 0:
            prueba_y = nuevo.copy()
            prueba_y.y += dy
            if not self.verificar_colision_multiple(prueba_y, self.hitboxes):
                nuevo.y += dy
            else:
                # no mover en Y
                pass

        return nuevo

    def dibujar_debug(self, screen, camara, color=(255, 0, 0), grosor=2):
        """
        Dibuja las hitboxes aplicando el offset de la cámara.
        camara: pygame.Vector2 con la posición de la cámara (en px).
        """
        if not self.debug_mode:
            return
        for r in self.hitboxes:
            draw_rect = pygame.Rect(r.x - camara.x, r.y - camara.y, r.width, r.height)
            pygame.draw.rect(screen, color, draw_rect, grosor)

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode
