# impacto_visual_mundo.py
"""
Sistema de impacto visual del mundo basado en consumo.
Transforma el entorno según las decisiones del jugador.

Patrón de diseño: Observer Pattern
- El mundo reacciona automáticamente a cambios en contaminación
- Componentes visuales se suscriben a cambios de estado
- Desacoplado y extensible

Características técnicas avanzadas:
- Generación procedural de basura
- Particle system para efectos atmosféricos
- Color grading dinámico
- Transiciones suaves entre estados
"""

import pygame
import random
import math
from typing import List, Tuple, Optional

class ParticulaBasura:
    """
    Partícula individual de basura generada proceduralmente.
    
    Características:
    - Posición y velocidad únicas
    - Tipo visual aleatorio
    - Fade in/out suave
    - Persistencia temporal
    """
    
    def __init__(self, x: float, y: float, tipo: int):
        self.x = x
        self.y = y
        self.tipo = tipo  # 0=botella, 1=bolsa, 2=lata, 3=papel
        self.alpha = 0
        self.target_alpha = random.randint(180, 255)
        self.fade_speed = random.uniform(2, 5)
        self.size = random.randint(15, 30)
        self.rotation = random.randint(0, 360)
        self.drift_speed = random.uniform(0.1, 0.3)
        self.drift_angle = random.uniform(0, 2 * math.pi)
        self.edad = 0
        self.max_edad = random.randint(300, 600)  # frames
        
        # Colores según tipo
        self.colores = [
            (100, 150, 100),  # Botella verde
            (200, 200, 200),  # Bolsa gris
            (180, 180, 200),  # Lata plateada
            (220, 200, 150)   # Papel amarillento
        ]
        self.color = self.colores[tipo]
    
    def actualizar(self, dt: int):
        """Actualiza estado de la partícula"""
        # Fade in
        if self.alpha < self.target_alpha:
            self.alpha = min(self.target_alpha, self.alpha + self.fade_speed)
        
        # Deriva lenta (simula viento)
        self.x += math.cos(self.drift_angle) * self.drift_speed
        self.y += math.sin(self.drift_angle) * self.drift_speed
        
        # Envejecimiento
        self.edad += 1
        
        # Fade out al final de vida
        if self.edad > self.max_edad * 0.8:
            fade_ratio = (self.edad - self.max_edad * 0.8) / (self.max_edad * 0.2)
            self.alpha = int(self.target_alpha * (1 - fade_ratio))
    
    def esta_viva(self) -> bool:
        """Verifica si la partícula sigue activa"""
        return self.edad < self.max_edad
    
    def dibujar(self, surface: pygame.Surface, camara):
        """Renderiza la partícula de basura"""
        screen_x = self.x - camara.x
        screen_y = self.y - camara.y
        
        # Solo dibujar si está en pantalla
        if -50 < screen_x < surface.get_width() + 50 and -50 < screen_y < surface.get_height() + 50:
            # Crear superficie con alpha
            basura_surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            
            # Dibujar según tipo
            if self.tipo == 0:  # Botella
                pygame.draw.ellipse(basura_surf, (*self.color, self.alpha), 
                                   (0, 0, self.size, self.size))
                pygame.draw.rect(basura_surf, (*self.color, self.alpha),
                                (self.size//3, 0, self.size//3, self.size//4))
            elif self.tipo == 1:  # Bolsa
                pygame.draw.polygon(basura_surf, (*self.color, self.alpha),
                                   [(0, self.size//2), (self.size//2, 0), 
                                    (self.size, self.size//2), (self.size//2, self.size)])
            elif self.tipo == 2:  # Lata
                pygame.draw.rect(basura_surf, (*self.color, self.alpha),
                                (0, 0, self.size, self.size), border_radius=3)
            else:  # Papel
                pygame.draw.rect(basura_surf, (*self.color, self.alpha),
                                (0, 0, self.size, int(self.size * 0.7)))
            
            # Blit con rotación
            rotated = pygame.transform.rotate(basura_surf, self.rotation)
            rect = rotated.get_rect(center=(screen_x, screen_y))
            surface.blit(rotated, rect)

class SistemaBasura:
    """
    Sistema procedural de generación de basura.
    
    Algoritmo:
    - Genera basura en zonas específicas del mapa
    - Densidad proporcional a contaminación
    - Pool de partículas para optimización
    """
    
    def __init__(self, mapa_width: int, mapa_height: int):
        self.mapa_width = mapa_width
        self.mapa_height = mapa_height
        self.particulas: List[ParticulaBasura] = []
        self.max_particulas = 150
        self.tiempo_desde_spawn = 0
        self.intervalo_spawn = 500  # ms
        
    def actualizar(self, dt: int, nivel_contaminacion: float):
        """
        Actualiza el sistema de basura.
        
        Args:
            dt: Delta time en ms
            nivel_contaminacion: 0-100
        """
        # Actualizar partículas existentes
        self.particulas = [p for p in self.particulas if p.esta_viva()]
        for particula in self.particulas:
            particula.actualizar(dt)
        
        # Generar nueva basura según contaminación
        self.tiempo_desde_spawn += dt
        
        if self.tiempo_desde_spawn >= self.intervalo_spawn:
            self.tiempo_desde_spawn = 0
            self._generar_basura(nivel_contaminacion)
    
    def _generar_basura(self, nivel_contaminacion: float):
        """Genera nuevas partículas de basura"""
        # Calcular cantidad a generar
        if nivel_contaminacion < 30:
            return  # No generar basura
        elif nivel_contaminacion < 60:
            cantidad = random.randint(0, 2)
        elif nivel_contaminacion < 85:
            cantidad = random.randint(1, 4)
        else:
            cantidad = random.randint(3, 6)
        
        # Generar partículas
        for _ in range(cantidad):
            if len(self.particulas) >= self.max_particulas:
                break
            
            # Posición aleatoria en el mapa
            x = random.uniform(0, self.mapa_width)
            y = random.uniform(0, self.mapa_height)
            tipo = random.randint(0, 3)
            
            self.particulas.append(ParticulaBasura(x, y, tipo))
    
    def dibujar(self, surface: pygame.Surface, camara):
        """Renderiza todas las partículas de basura"""
        for particula in self.particulas:
            particula.dibujar(surface, camara)
    
    def limpiar_todo(self):
        """Elimina toda la basura (acción de limpieza)"""
        self.particulas.clear()

class FiltroColorGrading:
    """
    Sistema de color grading dinámico basado en contaminación.
    
    Técnica:
    - Overlay con blend modes
    - Desaturación progresiva
    - Tint ambiental
    """
    
    def __init__(self, screen_size: tuple):
        self.width, self.height = screen_size
        self.overlay = pygame.Surface(screen_size, pygame.SRCALPHA)
    
    def aplicar(self, surface: pygame.Surface, nivel_contaminacion: float):
        """
        Aplica color grading según nivel de contaminación.
        
        Args:
            surface: Superficie donde aplicar el filtro
            nivel_contaminacion: 0-100
        """
        if nivel_contaminacion < 30:
            return  # No aplicar filtro
        
        # Calcular intensidad del filtro
        if nivel_contaminacion < 60:
            intensidad = (nivel_contaminacion - 30) / 30  # 0-1
            color = (50, 50, 50)  # Gris ligero
        elif nivel_contaminacion < 85:
            intensidad = (nivel_contaminacion - 60) / 25  # 0-1
            color = (40, 40, 35)  # Gris oscuro con tint marrón
        else:
            intensidad = min(1.0, (nivel_contaminacion - 85) / 15)
            color = (30, 25, 20)  # Muy oscuro y contaminado
        
        # Alpha del overlay
        alpha = int(intensidad * 120)
        
        # Crear overlay
        self.overlay.fill((*color, alpha))
        
        # Aplicar con blend mode
        surface.blit(self.overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

class IndicadorContaminacion:
    """
    Widget visual que muestra el nivel de contaminación en tiempo real.
    
    Diseño: Barra circular con animación suave
    """
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.radius = 45
        self.thickness = 8
        self.valor_actual = 0.0
        self.valor_objetivo = 0.0
        self.velocidad_lerp = 0.05
        
        # Fuentes
        self.font_valor = pygame.font.Font(None, 32)
        self.font_label = pygame.font.Font(None, 18)
        
        # Animación de pulso
        self.pulso_time = 0
        self.pulso_speed = 0.05
    
    def actualizar(self, nivel_contaminacion: float, dt: int):
        """Actualiza el indicador con interpolación suave"""
        self.valor_objetivo = nivel_contaminacion
        
        # Lerp hacia el objetivo
        if abs(self.valor_actual - self.valor_objetivo) > 0.1:
            self.valor_actual += (self.valor_objetivo - self.valor_actual) * self.velocidad_lerp
        else:
            self.valor_actual = self.valor_objetivo
        
        # Actualizar pulso
        self.pulso_time += self.pulso_speed * (dt / 16.67)  # Normalizar a 60fps
    
    def dibujar(self, surface: pygame.Surface):
        """Renderiza el indicador circular animado"""
        # Color según nivel
        if self.valor_actual < 30:
            color_principal = (80, 220, 80)
            color_fondo = (40, 110, 40)
            etiqueta = "BAJO"
        elif self.valor_actual < 60:
            color_principal = (255, 200, 60)
            color_fondo = (127, 100, 30)
            etiqueta = "MEDIO"
        elif self.valor_actual < 85:
            color_principal = (255, 140, 60)
            color_fondo = (127, 70, 30)
            etiqueta = "ALTO"
        else:
            color_principal = (255, 80, 80)
            color_fondo = (127, 40, 40)
            etiqueta = "CRÍTICO"
        
        # Fondo del indicador
        pygame.draw.circle(surface, (30, 30, 35), (self.x, self.y), self.radius + 5)
        
        # Círculo de fondo
        pygame.draw.circle(surface, color_fondo, (self.x, self.y), self.radius, self.thickness)
        
        # Arco de progreso
        angulo_inicio = -90  # Empezar arriba
        angulo_progreso = (self.valor_actual / 100) * 360
        
        if angulo_progreso > 0:
            self._dibujar_arco(surface, self.x, self.y, self.radius, 
                              angulo_inicio, angulo_inicio + angulo_progreso,
                              color_principal, self.thickness)
        
        # Efecto de pulso si está en nivel crítico
        if self.valor_actual >= 85:
            pulso_alpha = int((math.sin(self.pulso_time) + 1) * 60)
            pulso_radius = self.radius + 3
            self._dibujar_circulo_alpha(surface, self.x, self.y, pulso_radius,
                                       (*color_principal, pulso_alpha), 3)
        
        # Borde exterior
        pygame.draw.circle(surface, (200, 200, 200), (self.x, self.y), 
                          self.radius + self.thickness // 2, 2)
        
        # Valor numérico central
        texto_valor = f"{int(self.valor_actual)}"
        txt_surface = self.font_valor.render(texto_valor, True, color_principal)
        txt_rect = txt_surface.get_rect(center=(self.x, self.y - 5))
        surface.blit(txt_surface, txt_rect)
        
        # Etiqueta
        txt_label = self.font_label.render(etiqueta, True, (200, 200, 200))
        txt_rect = txt_label.get_rect(center=(self.x, self.y + 15))
        surface.blit(txt_label, txt_rect)
        
        # Icono
        icono = "🌍" if self.valor_actual < 60 else "🌫️"
        txt_icono = pygame.font.Font(None, 28).render(icono, True, (255, 255, 255))
        txt_rect = txt_icono.get_rect(center=(self.x, self.y - 60))
        surface.blit(txt_icono, txt_rect)
    
    def _dibujar_arco(self, surface, x, y, radius, start_angle, end_angle, color, thickness):
        """Dibuja un arco circular (helper method)"""
        # Convertir ángulos a radianes
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Calcular puntos del arco
        puntos = []
        steps = max(2, int(abs(end_angle - start_angle)))
        
        for i in range(steps + 1):
            angle = start_rad + (end_rad - start_rad) * (i / steps)
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            puntos.append((px, py))
        
        # Dibujar líneas conectadas
        if len(puntos) > 1:
            pygame.draw.lines(surface, color, False, puntos, thickness)
    
    def _dibujar_circulo_alpha(self, surface, x, y, radius, color, thickness):
        """Dibuja un círculo con transparencia"""
        temp_surface = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, color, (radius + 5, radius + 5), radius, thickness)
        surface.blit(temp_surface, (x - radius - 5, y - radius - 5))

class GestorImpactoVisual:
    """
    Coordinador principal de todos los efectos visuales del mundo.
    
    Patrón: Facade + Observer
    - Unifica todos los sistemas visuales
    - Reacciona automáticamente a cambios de contaminación
    - Proporciona interfaz simple para el main
    """
    
    def __init__(self, screen_size: tuple, mapa_size: tuple):
        self.screen_w, self.screen_h = screen_size
        self.mapa_w, self.mapa_h = mapa_size
        
        # Subsistemas
        self.sistema_basura = SistemaBasura(mapa_size[0], mapa_size[1])
        self.filtro_color = FiltroColorGrading(screen_size)
        self.indicador = IndicadorContaminacion(screen_size[0] - 80, 80)
        
        # Estado
        self.nivel_contaminacion = 0.0
        self.efectos_activos = False
    
    def actualizar(self, dt: int, nivel_contaminacion: float):
        """
        Actualiza todos los sistemas visuales.
        
        Args:
            dt: Delta time en ms
            nivel_contaminacion: 0-100
        """
        self.nivel_contaminacion = nivel_contaminacion
        self.efectos_activos = nivel_contaminacion >= 30
        
        # Actualizar subsistemas
        self.sistema_basura.actualizar(dt, nivel_contaminacion)
        self.indicador.actualizar(nivel_contaminacion, dt)
    
    def renderizar_capa_fondo(self, surface: pygame.Surface, camara):
        """
        Renderiza efectos que van DETRÁS del jugador.
        
        Llamar ANTES de dibujar jugador/NPCs.
        """
        if not self.efectos_activos:
            return
        
        # Basura en el suelo
        self.sistema_basura.dibujar(surface, camara)
    
    def renderizar_capa_overlay(self, surface: pygame.Surface):
        """
        Renderiza efectos que van ENCIMA de todo.
        
        Llamar DESPUÉS de dibujar todo el mundo.
        """
        if not self.efectos_activos:
            return
        
        # Filtro de color
        self.filtro_color.aplicar(surface, self.nivel_contaminacion)
    
    def renderizar_ui(self, surface: pygame.Surface):
        """
        Renderiza elementos de UI (indicador).
        
        Llamar al final, con la interfaz.
        """
        self.indicador.dibujar(surface)
    
    def accion_limpieza(self):
        """Ejecuta una acción de limpieza del mundo"""
        self.sistema_basura.limpiar_todo()
        print("[ImpactoVisual] Mundo limpiado")
    
    def get_estado_critico(self) -> bool:
        """Retorna True si la contaminación es crítica"""
        return self.nivel_contaminacion >= 85

# ====================================================================
# EFECTOS ADICIONALES: Partículas atmosféricas
# ====================================================================

class ParticulasAtmosfericas:
    """
    Sistema de partículas para efectos atmosféricos (humo, niebla).
    Aparece en niveles críticos de contaminación.
    """
    
    def __init__(self, screen_size: tuple):
        self.screen_w, self.screen_h = screen_size
        self.particulas = []
        self.activo = False
        self.max_particulas = 30
        self.tiempo_spawn = 0
    
    def actualizar(self, dt: int, nivel_contaminacion: float):
        """Actualiza partículas atmosféricas"""
        self.activo = nivel_contaminacion >= 85
        
        if not self.activo:
            self.particulas.clear()
            return
        
        # Actualizar existentes
        for p in self.particulas:
            p['y'] -= p['vel_y']
            p['x'] += p['vel_x']
            p['alpha'] = max(0, p['alpha'] - 0.5)
        
        # Remover muertas
        self.particulas = [p for p in self.particulas if p['alpha'] > 0]
        
        # Generar nuevas
        self.tiempo_spawn += dt
        if self.tiempo_spawn > 100 and len(self.particulas) < self.max_particulas:
            self.tiempo_spawn = 0
            self._spawn_particula()
    
    def _spawn_particula(self):
        """Genera una partícula de humo"""
        self.particulas.append({
            'x': random.uniform(0, self.screen_w),
            'y': self.screen_h + 20,
            'vel_x': random.uniform(-0.3, 0.3),
            'vel_y': random.uniform(0.5, 1.5),
            'size': random.randint(40, 80),
            'alpha': random.randint(30, 60),
            'color': random.choice([(100, 100, 90), (90, 90, 80), (80, 75, 70)])
        })
    
    def dibujar(self, surface: pygame.Surface):
        """Renderiza partículas atmosféricas"""
        if not self.activo:
            return
        
        for p in self.particulas:
            # Crear superficie con alpha
            size = p['size']
            particula_surf = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # Dibujar círculo difuminado (gradiente)
            for i in range(3):
                radio = size // 2 - (i * 5)
                alpha = int(p['alpha'] * (1 - i * 0.3))
                if radio > 0 and alpha > 0:
                    pygame.draw.circle(particula_surf, (*p['color'], alpha),
                                     (size // 2, size // 2), radio)
            
            # Blit
            surface.blit(particula_surf, (int(p['x'] - size // 2), int(p['y'] - size // 2)))