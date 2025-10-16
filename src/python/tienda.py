# tienda.py
import pygame
import math

class Item:
    def __init__(self, name, description="", price=0, effect=None):
        self.name = name
        self.description = description
        self.price = price
        self.effect = effect or {}

class Tienda:
    def __init__(self, items):
        self.items = items
        self.width = 420
        self.height = 300
        self.x = 100
        self.y = 80
        self.slot_height = 48
        self.close_rect = pygame.Rect(self.x + self.width - 30, self.y + 8, 24, 20)
        self.item_rects = []

    def draw(self, surface):
        box = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, (25,25,35), box, border_radius=8)
        pygame.draw.rect(surface, (200,200,200), box, 2, border_radius=8)
        pygame.draw.rect(surface, (180,60,60), self.close_rect, border_radius=4)
        font = pygame.font.Font(None, 24)
        txt_x = font.render("X", True, (255,255,255))
        surface.blit(txt_x, (self.close_rect.x + 6, self.close_rect.y - 2))
        self.item_rects = []
        sx = self.x + 12
        sy = self.y + 40
        for i, item in enumerate(self.items):
            r = pygame.Rect(sx, sy + i * (self.slot_height + 8), self.width - 24, self.slot_height)
            pygame.draw.rect(surface, (45,45,60), r, border_radius=6)
            pygame.draw.rect(surface, (120,120,140), r, 2, border_radius=6)
            name = font.render(f"{item.name} - ${item.price}", True, (255,255,255))
            surface.blit(name, (r.x + 6, r.y + 6))
            desc = font.render(str(item.description), True, (200,200,200))
            surface.blit(desc, (r.x + 6, r.y + 26))
            self.item_rects.append(r)

    def handle_event(self, event, dinero, jugador, inventario):
        """
        Retorna:
         - (True, 0, 0) si cerrar
         - (False, -precio, consumo_delta, item_name) si compró y agregó al inventario
         - None si no consumió evento
        Nota: la inflación (2%) se aplica después de cobrar; el precio cobrado es el previo.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self.close_rect.collidepoint(mx, my):
                return (True, 0, 0)
            for idx, r in enumerate(self.item_rects):
                if r.collidepoint(mx, my):
                    item = self.items[idx]
                    # precio actual (se cobra este)
                    precio_actual = item.price
                    if dinero >= precio_actual:
                        # intentar agregar al inventario
                        if inventario.agregar_objeto(item):
                            # calcular consumo delta (si existe)
                            consumo_delta = item.effect.get("consumo", 0)
                            # aplicar inflación: precio aumenta 2% redondeado hacia arriba
                            nuevo_precio = math.ceil(precio_actual * 1.02)
                            item.price = nuevo_precio
                            # retornamos el nombre del item para que el main lleve estadísticas
                            return (False, -precio_actual, consumo_delta, item.name)
                        else:
                            # sin espacio, no comprar
                            return (False, 0, 0)
                    else:
                        # sin dinero
                        return (False, 0, 0)
        return None
