import pygame
from compilados_py.Release import personaje as per
class Protagonista (per.Personaje):
    #Clase que se encarga de generar el personaje jugable:
    #Recibe movimiento, dinero, imagen de Sprite, posicion en X y Y, Velocidad
    def __init__ (self, movimiento, dinero, animaciones, eje_x, eje_y, velocidad):
        super().__init__(movimiento, dinero)
        self.eje_x = eje_x
        self.eje_y = eje_y
        self.velocidad = velocidad
        self.flip_x = False
        self.flip_y = False
        
        # Rectángulo de colisión del jugador
        self.rect = pygame.Rect(eje_x, eje_y, 105, 165)
        
        # Sistema de animaciones
        self.animaciones = animaciones
        self.frame_index = 0
        self.animation_speed = 0.1  # Velocidad de cambio de frame
        self.current_animation = "idle"
        self.last_update = pygame.time.get_ticks()
        
        # Estados de animación por dirección
        self.animation_states = {
            "idle": [0],           # Frame 0 para idle
            "up": [1],             # Frame 1 para arriba (W)
            "down": [4],           # Frame 4 para abajo (S)
            "left": [5, 6],        # Frames 5-6 para izquierda (A) - con flip
            "right": [5, 6]        # Frames 5-6 para derecha (D) - sin flip
        }

    def update_animation(self):
        """Actualiza la animación basada en el tiempo"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 1000:
            self.frame_index += 1
            self.last_update = current_time
            
            # Reiniciar el frame si llegamos al final
            if self.frame_index >= len(self.animation_states[self.current_animation]):
                self.frame_index = 0
    
    def set_animation(self, animation_name):
        """Cambia el estado de animación"""
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.frame_index = 0
    
    def get_current_frame(self):
        """Obtiene el frame actual de la animación"""
        frame_list = self.animation_states[self.current_animation]
        if frame_list:
            return self.animaciones[frame_list[self.frame_index]]
        return self.animaciones[0]  # Frame por defecto

    def movimiento (self, obstaculos=None):
        teclas = pygame.key.get_pressed()
        current_direction = "idle"
        
        # Guardar posición actual
        old_x = self.eje_x
        old_y = self.eje_y
        
        # Detectar dirección de movimiento
        if teclas[pygame.K_w]:
            self.eje_y -= self.velocidad
            current_direction = "up"
        elif teclas[pygame.K_s]:
            self.eje_y += self.velocidad
            current_direction = "down"
        elif teclas[pygame.K_a]:
            self.eje_x -= self.velocidad
            self.flip_x = True
            current_direction = "left"
        elif teclas[pygame.K_d]:
            self.eje_x += self.velocidad
            self.flip_x = False
            current_direction = "right"
        
        # Actualizar rectángulo de colisión
        self.rect.x = self.eje_x
        self.rect.y = self.eje_y
        
        # Verificar colisiones si se proporcionan obstáculos
        if obstaculos:
            for obstaculo in obstaculos:
                if self.rect.colliderect(obstaculo):
                    # Revertir movimiento si hay colisión
                    self.eje_x = old_x
                    self.eje_y = old_y
                    self.rect.x = self.eje_x
                    self.rect.y = self.eje_y
                    break
        
        # Cambiar animación según la dirección
        self.set_animation(current_direction)
        
        # Actualizar animación
        self.update_animation()

    def dibujar (self, interfaz):
        current_frame = self.get_current_frame()
        
        # Aplicar flip horizontal para las animaciones de izquierda
        if self.current_animation == "left":
            imagen_flip = pygame.transform.flip(current_frame, True, self.flip_y)
        else:
            imagen_flip = pygame.transform.flip(current_frame, self.flip_x, self.flip_y)
            
        interfaz.blit(imagen_flip, (self.eje_x, self.eje_y))

class NPC (per.Personaje):
    #clase que crea un NPC
    def __init__ (self, movimiento, dinero, eje_x, eje_y, dialogos):
        super().__init__(movimiento, dinero)
        self.eje_x = eje_x
        self.eje_y = eje_y
        self.dialogos = dialogos
        self.rect = pygame.Rect(eje_x, eje_y, 105, 165)

    def dialogo (self, dialogo):
        pass
    