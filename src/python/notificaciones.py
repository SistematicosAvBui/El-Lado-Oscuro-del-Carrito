# notificaciones.py - Sistema de notificaciones visuales
import pygame
import time

class Notificacion:
    def __init__(self, mensaje, tipo="info", duracion=3000):
        """
        tipo: "info", "success", "warning", "error"
        duracion: milisegundos que dura la notificación
        """
        self.mensaje = mensaje
        self.tipo = tipo
        self.duracion = duracion
        self.tiempo_inicio = pygame.time.get_ticks()
        self.activa = True
        
        # Colores según tipo
        self.colores = {
            "info": (100, 150, 255),
            "success": (80, 220, 80),
            "warning": (255, 200, 60),
            "error": (255, 80, 80)
        }
        
        self.color = self.colores.get(tipo, self.colores["info"])
        self.alpha = 255
        
    def actualizar(self):
        """Actualiza el estado de la notificación"""
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
        
        if tiempo_transcurrido >= self.duracion:
            self.activa = False
            return False
        
        # Fade out en los últimos 500ms
        if tiempo_transcurrido >= self.duracion - 500:
            self.alpha = int(255 * (self.duracion - tiempo_transcurrido) / 500)
        
        return True
    
    def dibujar(self, surface, y_offset=0):
        """Dibuja la notificación en pantalla"""
        if not self.activa:
            return
        
        font = pygame.font.Font(None, 28)
        texto = font.render(self.mensaje, True, (255, 255, 255))
        
        # Dimensiones
        padding = 20
        ancho = texto.get_width() + padding * 2
        alto = texto.get_height() + padding
        
        # Posición centrada horizontalmente, arriba
        screen_w = surface.get_width()
        x = (screen_w - ancho) // 2
        y = 60 + y_offset
        
        # Fondo con alpha
        fondo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        color_con_alpha = (*self.color, self.alpha)
        fondo.fill(color_con_alpha)
        surface.blit(fondo, (x, y))
        
        # Borde
        pygame.draw.rect(surface, (255, 255, 255, self.alpha), 
                        (x, y, ancho, alto), 3, border_radius=8)
        
        # Texto
        texto.set_alpha(self.alpha)
        surface.blit(texto, (x + padding, y + padding // 2))


class SistemaNotificaciones:
    def __init__(self):
        self.notificaciones = []
        self.max_notificaciones = 5
    
    def agregar(self, mensaje, tipo="info", duracion=3000):
        """Agrega una nueva notificación"""
        notif = Notificacion(mensaje, tipo, duracion)
        self.notificaciones.append(notif)
        
        # Limitar cantidad de notificaciones
        if len(self.notificaciones) > self.max_notificaciones:
            self.notificaciones.pop(0)
        
        print(f"[Notificación {tipo.upper()}] {mensaje}")
    
    def actualizar(self):
        """Actualiza todas las notificaciones"""
        # Remover notificaciones inactivas
        self.notificaciones = [n for n in self.notificaciones if n.actualizar()]
    
    def dibujar(self, surface):
        """Dibuja todas las notificaciones activas"""
        y_offset = 0
        for notif in self.notificaciones:
            notif.dibujar(surface, y_offset)
            y_offset += 70  # Espaciado entre notificaciones
    
    def limpiar(self):
        """Limpia todas las notificaciones"""
        self.notificaciones.clear()