# ui.py
import pygame

class UI:
    def __init__(self, pos_x=50, pos_y=50):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 24)
        self.color_texto = (255,255,255)
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.inv_width = 500
        self.inv_height = 250
        self.slot_cols = 5
        self.slot_rows = 2
        self.slot_spacing = 10
        self.slot_rects = []
        self.submenu_rect = pygame.Rect(0,0,140,60)
        self.accion_usar_rect = pygame.Rect(0,0,60,30)
        self.accion_vender_rect = pygame.Rect(0,0,60,30)

    def interfaz_inventario(self, surface, capacidad):
        return self.draw_inventory(surface, None)

    def draw_inventory(self, surface, inventario, slot_selected=None, open_submenu=False):
        x = (surface.get_width() - self.inv_width) // 2
        y = (surface.get_height() - self.inv_height) // 2
        inv_rect = pygame.Rect(x,y,self.inv_width,self.inv_height)
        pygame.draw.rect(surface, (30,30,30), inv_rect, border_radius=8)
        pygame.draw.rect(surface, (200,200,200), inv_rect, 2, border_radius=8)
        cerrar_rect = pygame.Rect(inv_rect.right - 30, inv_rect.top + 6, 24, 20)
        pygame.draw.rect(surface, (180,60,60), cerrar_rect, border_radius=4)
        txt_x = self.font.render("X", True, (255,255,255))
        surface.blit(txt_x, (cerrar_rect.x+6, cerrar_rect.y-2))

        ancho_slot = (self.inv_width - (self.slot_spacing * (self.slot_cols + 1))) // self.slot_cols
        alto_slot = (self.inv_height - 60 - (self.slot_spacing * (self.slot_rows + 1))) // self.slot_rows
        slots = []
        base_x = x + self.slot_spacing
        base_y = y + 40

        index = 0
        total_slots = self.slot_cols * self.slot_rows
        for r in range(self.slot_rows):
            for c in range(self.slot_cols):
                sx = base_x + c * (ancho_slot + self.slot_spacing)
                sy = base_y + r * (alto_slot + self.slot_spacing)
                rect = pygame.Rect(sx, sy, ancho_slot, alto_slot)
                pygame.draw.rect(surface, (50,50,50), rect)
                pygame.draw.rect(surface, (150,150,150), rect, 2)
                try:
                    item = inventario.contenido[index]
                except Exception:
                    item = None
                if item:
                    inner = rect.inflate(-8, -8)
                    pygame.draw.rect(surface, (100,120,180), inner)
                    name_s = self.font.render(str(item.name), True, (255,255,255))
                    surface.blit(name_s, (inner.x + 4, inner.y + 4))
                if slot_selected is not None and slot_selected == index:
                    pygame.draw.rect(surface, (255,255,0), rect, 3)
                slots.append(rect)
                index += 1

        self.slot_rects = slots
        cap_txt = self.font.render(f"Espacios libres: {inventario.capacidad}", True, (255,255,255))
        surface.blit(cap_txt, (inv_rect.left + 8, inv_rect.top + 8))
        return {"inv_rect": inv_rect, "slots": slots, "close_rect": cerrar_rect}

    def handle_event_inventory(self, event, inventario):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            info = self.draw_inventory(self.display_surface, inventario)
            mx,my = event.pos
            if info["close_rect"].collidepoint(mx,my):
                return (True, None, False)
            for idx, rect in enumerate(info["slots"]):
                if rect.collidepoint(mx,my):
                    return (False, idx, True)
            return None
        return None

    def draw_submenu(self, surface):
        w,h = 140,60
        x = surface.get_width() - w - 20
        y = surface.get_height() - h - 20
        self.submenu_rect = pygame.Rect(x,y,w,h)
        pygame.draw.rect(surface, (40,40,40), self.submenu_rect, border_radius=6)
        pygame.draw.rect(surface, (200,200,200), self.submenu_rect, 2, border_radius=6)
        usar = pygame.Rect(x + 10, y + 12, 60, 30)
        vender = pygame.Rect(x + 70, y + 12, 60, 30)
        self.accion_usar_rect = usar
        self.accion_vender_rect = vender
        pygame.draw.rect(surface, (70,130,70), usar, border_radius=6)
        pygame.draw.rect(surface, (130,70,70), vender, border_radius=6)
        usar_txt = self.font.render("Usar", True, (255,255,255))
        vender_txt = self.font.render("Vender", True, (255,255,255))
        surface.blit(usar_txt, (usar.x + 10, usar.y + 6))
        surface.blit(vender_txt, (vender.x + 6, vender.y + 6))

    def check_submenu_click(self, mx, my):
        if self.accion_usar_rect.collidepoint(mx,my):
            return "usar"
        if self.accion_vender_rect.collidepoint(mx,my):
            return "vender"
        return None

    def barras_estado_simple(self, surface, label, valor, x, y):
        maximo = 100
        ancho_max = 160
        alto = 12
        pygame.draw.rect(surface, (0,0,0), (x,y,ancho_max,alto))
        porcentaje = max(0, min(1, valor / maximo))
        ancho_actual = int(ancho_max * porcentaje)
        if porcentaje > 0.6:
            color = (0,200,0)
        elif porcentaje > 0.3:
            color = (200,200,0)
        else:
            color = (200,50,50)
        pygame.draw.rect(surface, color, (x,y,ancho_actual,alto))
        txt = self.font.render(f"{label}: {int(valor)}", True, (255,255,255))
        surface.blit(txt, (x + ancho_max + 6, y - 2))
