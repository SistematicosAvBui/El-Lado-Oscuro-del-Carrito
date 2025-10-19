# popup_decision.py
"""
Sistema de popups para la mecánica "Necesidad vs Deseo".
Muestra reflexiones antes de confirmar compras.

Principio DRY: Reutilizable para cualquier decisión reflexiva del juego.
"""

import pygame
from typing import Optional, Callable, Dict

class PopupDecision:
    """
    Popup modal que fuerza al jugador a reflexionar antes de comprar.
    
    Características:
    - Bloquea input hasta que se tome una decisión
    - Animación de entrada suave
    - Diseño coherente con la UI del juego
    - Callbacks para confirmar/cancelar
    """
    
    def __init__(self, screen_size: tuple):
        self.screen_w, self.screen_h = screen_size
        self.activo = False
        self.alpha = 0  # Para fade-in
        self.target_alpha = 240
        
        # Dimensiones del popup
        self.width = min(600, int(self.screen_w * 0.7))
        self.height = min(400, int(self.screen_h * 0.6))
        self.x = (self.screen_w - self.width) // 2
        self.y = (self.screen_h - self.height) // 2
        
        # Fuentes
        self.font_titulo = pygame.font.Font(None, 42)
        self.font_mensaje = pygame.font.Font(None, 28)
        self.font_boton = pygame.font.Font(None, 30)
        
        # Contenido
        self.titulo = ""
        self.mensaje = ""
        self.producto_nombre = ""
        self.impacto_color = (255, 200, 60)
        
        # Botones
        self.btn_width = 200
        self.btn_height = 50
        self.btn_spacing = 20
        
        self.btn_confirmar = pygame.Rect(0, 0, self.btn_width, self.btn_height)
        self.btn_cancelar = pygame.Rect(0, 0, self.btn_width, self.btn_height)
        
        # Callbacks
        self.callback_confirmar: Optional[Callable] = None
        self.callback_cancelar: Optional[Callable] = None
        
        # Animación
        self.tiempo_apertura = 0
        self.duracion_fade = 300  # ms
    
    def abrir(self, producto: str, info_decision: Dict, 
              on_confirmar: Callable, on_cancelar: Callable):
        """
        Abre el popup con información de decisión.
        
        Args:
            producto: Nombre del producto
            info_decision: Dict con "tipo", "impacto", "mensaje", etc.
            on_confirmar: Callback si confirma compra
            on_cancelar: Callback si cancela
        """
        self.activo = True
        self.alpha = 0
        self.tiempo_apertura = pygame.time.get_ticks()
        
        self.producto_nombre = producto
        self.mensaje = info_decision.get("mensaje", "¿Realmente necesitas esto?")
        self.impacto_color = info_decision.get("color_impacto", (255, 200, 60))
        
        # Título según tipo de producto
        tipo = info_decision.get("tipo")
        if tipo and "NECESIDAD" in str(tipo):
            self.titulo = "💚 Necesidad Identificada"
        else:
            self.titulo = "⚠️ ¿Necesidad o Deseo?"
        
        self.callback_confirmar = on_confirmar
        self.callback_cancelar = on_cancelar
        
        # Posicionar botones
        total_width = self.btn_width * 2 + self.btn_spacing
        btn_y = self.y + self.height - 80
        
        self.btn_cancelar.x = self.x + (self.width - total_width) // 2
        self.btn_cancelar.y = btn_y
        
        self.btn_confirmar.x = self.btn_cancelar.right + self.btn_spacing
        self.btn_confirmar.y = btn_y
        
        print(f"[PopupDecision] Abierto para: {producto}")
    
    def cerrar(self):
        """Cierra el popup"""
        self.activo = False
        self.alpha = 0
        print("[PopupDecision] Cerrado")
    
    def actualizar(self, dt: int):
        """Actualiza la animación del popup"""
        if not self.activo:
            return
        
        # Fade-in
        tiempo_actual = pygame.time.get_ticks()
        tiempo_desde_apertura = tiempo_actual - self.tiempo_apertura
        
        if tiempo_desde_apertura < self.duracion_fade:
            ratio = tiempo_desde_apertura / self.duracion_fade
            self.alpha = int(self.target_alpha * ratio)
        else:
            self.alpha = self.target_alpha
    
    def manejar_evento(self, event: pygame.event.Event) -> bool:
        """
        Maneja eventos del popup.
        
        Returns:
            True si el evento fue consumido (bloquea input del juego)
        """
        if not self.activo:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            
            # Click en confirmar
            if self.btn_confirmar.collidepoint(mx, my):
                print(f"[PopupDecision] CONFIRMADO: {self.producto_nombre}")
                if self.callback_confirmar:
                    self.callback_confirmar()
                self.cerrar()
                return True
            
            # Click en cancelar
            if self.btn_cancelar.collidepoint(mx, my):
                print(f"[PopupDecision] CANCELADO: {self.producto_nombre}")
                if self.callback_cancelar:
                    self.callback_cancelar()
                self.cerrar()
                return True
        
        # Tecla ESC = cancelar
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.callback_cancelar:
                self.callback_cancelar()
            self.cerrar()
            return True
        
        # Consumir todos los eventos mientras esté activo
        return True
    
    def dibujar(self, surface: pygame.Surface):
        """Renderiza el popup"""
        if not self.activo or self.alpha == 0:
            return
        
        # Overlay oscuro de fondo
        overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(self.alpha * 0.7)))
        surface.blit(overlay, (0, 0))
        
        # Caja del popup
        popup_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        popup_surface.fill((40, 40, 50, self.alpha))
        
        # Borde con color de impacto
        border_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(popup_surface, self.impacto_color, border_rect, 5, border_radius=15)
        
        # Título
        titulo_surface = self.font_titulo.render(self.titulo, True, (255, 255, 255))
        titulo_surface.set_alpha(self.alpha)
        titulo_x = (self.width - titulo_surface.get_width()) // 2
        popup_surface.blit(titulo_surface, (titulo_x, 30))
        
        # Nombre del producto
        producto_surface = self.font_mensaje.render(
            f'"{self.producto_nombre}"', 
            True, 
            self.impacto_color
        )
        producto_surface.set_alpha(self.alpha)
        producto_x = (self.width - producto_surface.get_width()) // 2
        popup_surface.blit(producto_surface, (producto_x, 90))
        
        # Mensaje reflexivo (multilinea)
        self._dibujar_texto_multilinea(
            popup_surface,
            self.mensaje,
            pygame.Rect(40, 140, self.width - 80, 120),
            self.font_mensaje,
            (220, 220, 220)
        )
        
        # Botones
        mx, my = pygame.mouse.get_pos()
        mx_local = mx - self.x
        my_local = my - self.y
        
        # Botón Cancelar
        btn_cancelar_local = pygame.Rect(
            self.btn_cancelar.x - self.x,
            self.btn_cancelar.y - self.y,
            self.btn_width,
            self.btn_height
        )
        
        hover_cancelar = btn_cancelar_local.collidepoint(mx_local, my_local)
        color_cancelar = (220, 90, 90) if hover_cancelar else (180, 70, 70)
        pygame.draw.rect(popup_surface, color_cancelar, btn_cancelar_local, border_radius=10)
        pygame.draw.rect(popup_surface, (255, 255, 255), btn_cancelar_local, 3, border_radius=10)
        
        txt_cancelar = self.font_boton.render("Cancelar", True, (255, 255, 255))
        txt_cancelar.set_alpha(self.alpha)
        txt_x = btn_cancelar_local.x + (btn_cancelar_local.width - txt_cancelar.get_width()) // 2
        txt_y = btn_cancelar_local.y + (btn_cancelar_local.height - txt_cancelar.get_height()) // 2
        popup_surface.blit(txt_cancelar, (txt_x, txt_y))
        
        # Botón Confirmar
        btn_confirmar_local = pygame.Rect(
            self.btn_confirmar.x - self.x,
            self.btn_confirmar.y - self.y,
            self.btn_width,
            self.btn_height
        )
        
        hover_confirmar = btn_confirmar_local.collidepoint(mx_local, my_local)
        color_confirmar = (90, 220, 90) if hover_confirmar else (70, 180, 70)
        pygame.draw.rect(popup_surface, color_confirmar, btn_confirmar_local, border_radius=10)
        pygame.draw.rect(popup_surface, (255, 255, 255), btn_confirmar_local, 3, border_radius=10)
        
        txt_confirmar = self.font_boton.render("Comprar", True, (255, 255, 255))
        txt_confirmar.set_alpha(self.alpha)
        txt_x = btn_confirmar_local.x + (btn_confirmar_local.width - txt_confirmar.get_width()) // 2
        txt_y = btn_confirmar_local.y + (btn_confirmar_local.height - txt_confirmar.get_height()) // 2
        popup_surface.blit(txt_confirmar, (txt_x, txt_y))
        
        # Blit del popup en la pantalla
        surface.blit(popup_surface, (self.x, self.y))
    
    def _dibujar_texto_multilinea(self, surface, texto, rect, font, color):
        """Helper para dibujar texto con wrapping"""
        palabras = texto.split(' ')
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            test_linea = linea_actual + palabra + " "
            if font.size(test_linea)[0] < rect.width:
                linea_actual = test_linea
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                linea_actual = palabra + " "
        
        if linea_actual:
            lineas.append(linea_actual)
        
        # Renderizar líneas
        y_offset = rect.y
        for linea in lineas[:4]:  # Máximo 4 líneas
            linea_surface = font.render(linea.strip(), True, color)
            linea_surface.set_alpha(self.alpha)
            x_centered = rect.x + (rect.width - linea_surface.get_width()) // 2
            surface.blit(linea_surface, (x_centered, y_offset))
            y_offset += font.get_height() + 5