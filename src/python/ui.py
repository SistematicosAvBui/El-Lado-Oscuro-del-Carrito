# ui.py - VERSIÓN CORREGIDA CON SUBMENU FUNCIONAL
import pygame

class UI:
    def __init__(self, pos_x=50, pos_y=50):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        self.color_texto = (255, 255, 255)
        self.pos_x = pos_x
        self.pos_y = pos_y

        # Dimensiones responsive
        screen_w, screen_h = self.display_surface.get_size()
        self.inv_width = min(600, int(screen_w * 0.7))
        self.inv_height = min(350, int(screen_h * 0.6))
        
        self.slot_cols = 5
        self.slot_rows = 2
        self.slot_spacing = 10
        self.slot_rects = []
        
        # Submenu
        self.submenu_rect = pygame.Rect(0, 0, 160, 100)
        self.accion_usar_rect = pygame.Rect(0, 0, 140, 40)
        self.accion_vender_rect = pygame.Rect(0, 0, 140, 40)
        
        # FIX: Almacenar posición del slot seleccionado
        self.selected_slot_rect = None

    def interfaz_inventario(self, surface, capacidad):
        """Compatibilidad con código antiguo"""
        return self.draw_inventory(surface, None)

    def draw_inventory(self, surface, inventario, slot_selected=None, open_submenu=False):
        """
        Inventario centrado y responsive
        FIX: Se redibuja completamente cada frame para reflejar cambios
        """
        if inventario is None:
            return {"inv_rect": pygame.Rect(0,0,0,0), "slots": [], "close_rect": pygame.Rect(0,0,0,0)}
        
        screen_w, screen_h = surface.get_size()
        
        # Centrar inventario
        x = (screen_w - self.inv_width) // 2
        y = (screen_h - self.inv_height) // 2
        
        inv_rect = pygame.Rect(x, y, self.inv_width, self.inv_height)
        
        # Fondo con transparencia
        s = pygame.Surface((self.inv_width, self.inv_height), pygame.SRCALPHA)
        s.fill((30, 30, 30, 240))
        surface.blit(s, (x, y))
        
        # Borde
        pygame.draw.rect(surface, (200, 200, 200), inv_rect, 3, border_radius=10)
        
        # Título
        titulo = self.font.render("INVENTARIO", True, (255, 255, 255))
        surface.blit(titulo, (inv_rect.centerx - titulo.get_width()//2, y + 10))
        
        # Botón cerrar (X)
        cerrar_rect = pygame.Rect(inv_rect.right - 35, inv_rect.top + 10, 28, 28)
        pygame.draw.rect(surface, (180, 60, 60), cerrar_rect, border_radius=6)
        txt_x = self.font.render("X", True, (255, 255, 255))
        surface.blit(txt_x, (cerrar_rect.x + 8, cerrar_rect.y + 2))

        # Cálculo de slots
        padding_top = 50
        padding_bottom = 45
        area_slots_h = self.inv_height - padding_top - padding_bottom
        
        ancho_slot = (self.inv_width - (self.slot_spacing * (self.slot_cols + 1))) // self.slot_cols
        alto_slot = (area_slots_h - (self.slot_spacing * (self.slot_rows + 1))) // self.slot_rows
        
        # Validación de tamaño mínimo
        ancho_slot = max(60, ancho_slot)
        alto_slot = max(50, alto_slot)
        
        slots = []
        base_x = x + self.slot_spacing
        base_y = y + padding_top

        index = 0
        total_slots = self.slot_cols * self.slot_rows
        
        for r in range(self.slot_rows):
            for c in range(self.slot_cols):
                sx = base_x + c * (ancho_slot + self.slot_spacing)
                sy = base_y + r * (alto_slot + self.slot_spacing)
                rect = pygame.Rect(sx, sy, ancho_slot, alto_slot)
                
                # Slot vacío
                pygame.draw.rect(surface, (50, 50, 50), rect, border_radius=6)
                pygame.draw.rect(surface, (150, 150, 150), rect, 2, border_radius=6)
                
                # Verificar item
                item = None
                if inventario and index < len(inventario.contenido):
                    try:
                        item = inventario.contenido[index]
                    except (IndexError, AttributeError):
                        item = None
                
                if item:
                    # Item presente
                    inner = rect.inflate(-8, -8)
                    pygame.draw.rect(surface, (100, 120, 180), inner, border_radius=4)
                    
                    # Nombre del item
                    name_text = str(getattr(item, 'name', 'Item'))
                    if len(name_text) > 10:
                        name_text = name_text[:9] + "..."
                    
                    name_s = self.font_small.render(name_text, True, (255, 255, 255))
                    text_x = inner.x + (inner.width - name_s.get_width()) // 2
                    text_y = inner.y + (inner.height - name_s.get_height()) // 2
                    surface.blit(name_s, (text_x, text_y))
                
                # Highlight si está seleccionado
                if slot_selected is not None and slot_selected == index:
                    pygame.draw.rect(surface, (255, 255, 0), rect, 4, border_radius=6)
                    # FIX: Guardar rect del slot seleccionado
                    self.selected_slot_rect = rect
                
                slots.append(rect)
                index += 1

        self.slot_rects = slots
        
        # Info de capacidad
        if inventario:
            espacios_usados = len(inventario.contenido)
            cap_max = inventario.capacidad_maxima
            cap_txt = self.font_small.render(
                f"Espacios: {espacios_usados}/{cap_max}", 
                True, 
                (200, 200, 200)
            )
            surface.blit(cap_txt, (inv_rect.left + 10, inv_rect.bottom - 30))
        
        return {"inv_rect": inv_rect, "slots": slots, "close_rect": cerrar_rect}

    def handle_event_inventory(self, event, inventario):
        """
        Manejo de eventos del inventario
        Retorna: (cerrar, slot_idx, abrir_submenu)
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            info = self.draw_inventory(self.display_surface, inventario)
            mx, my = event.pos
            
            # Click en X (cerrar)
            if info["close_rect"].collidepoint(mx, my):
                return (True, None, False)
            
            # Click en slot
            for idx, rect in enumerate(info["slots"]):
                if rect.collidepoint(mx, my):
                    # Verificar que el slot tenga un item
                    if idx < len(inventario.contenido):
                        return (False, idx, True)
                    else:
                        # Slot vacío
                        return (False, None, False)
            
            return None
        return None

    def draw_submenu(self, surface):
        """
        FIX: Submenu posicionado cerca del slot seleccionado
        """
        if self.selected_slot_rect is None:
            return
        
        screen_w, screen_h = surface.get_size()
        
        w, h = 160, 100
        
        # Posicionar a la derecha del slot seleccionado
        x = self.selected_slot_rect.right + 15
        y = self.selected_slot_rect.top
        
        # Ajustar si se sale de la pantalla
        if x + w > screen_w:
            x = self.selected_slot_rect.left - w - 15
        if y + h > screen_h:
            y = screen_h - h - 10
        
        self.submenu_rect = pygame.Rect(x, y, w, h)
        
        # Fondo semi-transparente
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((40, 40, 40, 250))
        surface.blit(s, (x, y))
        
        # Borde
        pygame.draw.rect(surface, (255, 255, 255), self.submenu_rect, 3, border_radius=8)
        
        # Botones
        btn_width = 140
        btn_height = 38
        padding = 10
        
        usar = pygame.Rect(x + padding, y + padding, btn_width, btn_height)
        vender = pygame.Rect(x + padding, y + padding + btn_height + 6, btn_width, btn_height)
        
        self.accion_usar_rect = usar
        self.accion_vender_rect = vender
        
        # Dibujar botones con efecto hover
        mx, my = pygame.mouse.get_pos()
        
        # Botón Usar
        if usar.collidepoint(mx, my):
            pygame.draw.rect(surface, (90, 220, 90), usar, border_radius=6)
        else:
            pygame.draw.rect(surface, (70, 180, 70), usar, border_radius=6)
        pygame.draw.rect(surface, (255, 255, 255), usar, 2, border_radius=6)
        
        # Botón Vender
        if vender.collidepoint(mx, my):
            pygame.draw.rect(surface, (220, 90, 90), vender, border_radius=6)
        else:
            pygame.draw.rect(surface, (180, 70, 70), vender, border_radius=6)
        pygame.draw.rect(surface, (255, 255, 255), vender, 2, border_radius=6)
        
        # Texto de botones
        usar_txt = self.font.render("Usar", True, (255, 255, 255))
        vender_txt = self.font.render("Vender", True, (255, 255, 255))
        
        # Centrar texto en botones
        surface.blit(usar_txt, (usar.x + (usar.width - usar_txt.get_width())//2, 
                                usar.y + (usar.height - usar_txt.get_height())//2))
        surface.blit(vender_txt, (vender.x + (vender.width - vender_txt.get_width())//2, 
                                  vender.y + (vender.height - vender_txt.get_height())//2))

    def check_submenu_click(self, mx, my):
        """
        FIX: Verificación mejorada de clicks
        """
        # Verificar si el click está dentro del área del submenu
        if not self.submenu_rect.collidepoint(mx, my):
            return "close"  # Click fuera del submenu = cerrar
        
        if self.accion_usar_rect.collidepoint(mx, my):
            return "usar"
        if self.accion_vender_rect.collidepoint(mx, my):
            return "vender"
        return None

    def barras_estado_simple(self, surface, label, valor, x, y):
        """
        Barras de estado mejoradas
        """
        maximo = 100
        ancho_max = 160
        alto = 16
        
        # Fondo de la barra
        pygame.draw.rect(surface, (40, 40, 40), (x, y, ancho_max, alto), border_radius=4)
        
        # Barra de progreso
        porcentaje = max(0, min(1, valor / maximo))
        ancho_actual = int(ancho_max * porcentaje)
        
        # Color según porcentaje
        if porcentaje > 0.6:
            color = (50, 200, 50)
        elif porcentaje > 0.3:
            color = (220, 180, 0)
        else:
            color = (200, 50, 50)
        
        if ancho_actual > 0:
            pygame.draw.rect(surface, color, (x, y, ancho_actual, alto), border_radius=4)
        
        # Borde
        pygame.draw.rect(surface, (255, 255, 255), (x, y, ancho_max, alto), 2, border_radius=4)
        
        # Texto con valor
        txt = self.font_small.render(f"{label}: {int(valor)}", True, (255, 255, 255))
        surface.blit(txt, (x + ancho_max + 8, y - 2))