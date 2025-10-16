"""
Ejemplo de Integración de Sistemas para "El Lado Oscuro del Carrito"

Este archivo muestra cómo integrar todos los nuevos sistemas en el juego principal,
manteniendo la compatibilidad con el código existente.
"""

import pygame
import sys
import time
from typing import Optional

# Importar sistemas existentes
import jugador as per
import npc
import dialogos

# Importar nuevos sistemas
from sistemas.game_manager import get_game_manager
from sistemas.map_manager import MapManager, MapState
from sistemas.inventory_system import InventorySystem, Product, ItemType, ItemRarity


class EnhancedGame:
    """
    Clase principal del juego mejorado que integra todos los sistemas.
    
    Mantiene la compatibilidad con el código existente mientras
    añade las nuevas funcionalidades.
    """
    
    def __init__(self):
        """Inicializa el juego mejorado."""
        pygame.init()
        
        # Configuración de pantalla
        self.screen_size = (1200, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("El Lado Oscuro del Carrito - Enhanced")
        self.clock = pygame.time.Clock()
        
        # Estados del juego
        self.MENU = "menu"
        self.JUGANDO = "jugando"
        self.estado_actual = self.MENU
        
        # Inicializar GameManager
        self.game_manager = get_game_manager()
        
        # Cargar recursos
        self._load_resources()
        
        # Inicializar sistemas
        self._initialize_systems()
        
        # Configuración de UI
        self.fuente_dialogo = pygame.font.Font(None, 32)
        self.fuente_interaccion = pygame.font.Font(None, 40)
        
        # Estado del diálogo
        self.dialogo_activo = None
        self.dialogo_en_progreso = False
        
        # Cámara
        self.camara = pygame.Vector2(0, 0)
    
    def _load_resources(self):
        """Carga los recursos del juego."""
        # Cargar animaciones del jugador
        self.animaciones = []
        for frame in range(7):
            try:
                img = pygame.image.load(f"assets/{frame}-Photoroom.png").convert_alpha()
                img = pygame.transform.scale(img, (110, 130))
                self.animaciones.append(img)
            except pygame.error:
                # Crear placeholder si no se puede cargar
                placeholder = pygame.Surface((110, 130))
                placeholder.fill((100, 100, 100))
                self.animaciones.append(placeholder)
        
        # Cargar fondos
        try:
            self.fondo_menu = pygame.image.load("assets/imagen_fondo_principal.jpg")
            self.fondo_menu = pygame.transform.scale(self.fondo_menu, self.screen_size)
        except pygame.error:
            self.fondo_menu = pygame.Surface(self.screen_size)
            self.fondo_menu.fill((50, 50, 100))
    
    def _initialize_systems(self):
        """Inicializa todos los sistemas del juego."""
        # Crear jugador
        aparicion_x, aparicion_y = 250, 350
        dinero = 1500
        self.jugador = per.Protagonista(0, dinero, self.animaciones, aparicion_x, aparicion_y, 5)
        
        # Crear inventario mejorado
        self.inventario = InventorySystem(capacity=20)
        
        # Configurar referencias en GameManager
        self.game_manager.set_player_reference(self.jugador)
        self.game_manager.set_inventory_reference(self.inventario)
        
        # Inicializar sistemas del GameManager
        self.game_manager.initialize_systems()
        
        # Crear MapManager
        self.map_manager = MapManager()
        self.map_manager.set_player_reference(self.jugador)
        self.map_manager.set_game_manager_reference(self.game_manager)
        
        # Crear NPC vendedor
        self._create_vendor_npc()
        
        # Crear productos de ejemplo
        self._create_sample_products()
    
    def _create_vendor_npc(self):
        """Crea el NPC vendedor."""
        dialogos_vendedor = [
            "¡Hola, joven consumidor!",
            "Parece que tienes dinero fresco...",
            "Aquí todo está en oferta... aunque no por mucho tiempo.",
            "Recuerda: ¡comprar es invertir en la felicidad del sistema!"
        ]
        
        try:
            imagen_vendedor = pygame.image.load("assets/imagen_vendedor.png").convert_alpha()
            sprite_vendedor = pygame.transform.scale(imagen_vendedor, (100, 120))
        except pygame.error:
            sprite_vendedor = pygame.Surface((100, 120))
            sprite_vendedor.fill((255, 0, 0))
        
        self.vendedor = npc.NPC(0, 9999, 600, 350, dialogos_vendedor, sprite_vendedor)
    
    def _create_sample_products(self):
        """Crea productos de ejemplo para demostrar el sistema."""
        # Producto consumista
        smartphone = Product(
            "smartphone", "Smartphone Premium", 
            "El último modelo con todas las funciones innecesarias",
            999, ItemType.LUXURY, ItemRarity.RARE,
            effects={"satisfaction": 25, "real_happiness": -10}
        )
        
        # Producto esencial
        comida = Product(
            "comida", "Comida Básica",
            "Alimento nutritivo para sobrevivir",
            50, ItemType.ESSENTIAL, ItemRarity.COMMON,
            effects={"energia": 20, "real_happiness": 5}
        )
        
        # Producto de redención
        ropa_donacion = Product(
            "ropa_donacion", "Ropa para Donar",
            "Ropa en buen estado que puedes donar",
            0, ItemType.REDEMPTION, ItemRarity.COMMON,
            effects={"real_happiness": 15}
        )
        
        # Añadir productos al inventario del vendedor (simulado)
        self.productos_tienda = [smartphone, comida, ropa_donacion]
    
    def handle_events(self):
        """Maneja los eventos del juego."""
        dt = self.clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            # Cambio de estado
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.estado_actual == self.MENU:
                    self.estado_actual = self.JUGANDO
                    self.game_manager.change_game_state(self.game_manager.game_state.PLAYING)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.estado_actual == self.JUGANDO:
                    self.estado_actual = self.MENU
                    self.game_manager.change_game_state(self.game_manager.game_state.MENU)
            
            # Interacción con NPC
            if (self.estado_actual == self.JUGANDO and 
                event.type == pygame.KEYDOWN and 
                event.key == pygame.K_e and 
                self.jugador.rect.colliderect(self.vendedor.rect)):
                
                if not self.dialogo_en_progreso:
                    self.dialogo_activo = dialogos.Dialogo(
                        self.vendedor.dialogos, self.fuente_dialogo, 100, 450, 1000, 120
                    )
                    self.dialogo_en_progreso = True
            
            elif (event.type == pygame.KEYDOWN and 
                  event.key == pygame.K_SPACE and 
                  self.dialogo_en_progreso and 
                  self.dialogo_activo):
                self.dialogo_activo.siguiente_linea()
            
            # Manejar entrada de sistemas
            self.game_manager.handle_input(event)
            self.inventario.handle_input(event)
            
            # Teclas especiales
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.inventario.toggle_visibility()
                elif event.key == pygame.K_m:
                    # Cambiar de mapa (ejemplo)
                    if self.map_manager.current_state == MapState.VILLAGE:
                        self.map_manager.change_map(MapState.MARKETPLACE)
                    else:
                        self.map_manager.change_map(MapState.VILLAGE)
        
        return dt
    
    def update(self, dt):
        """Actualiza la lógica del juego."""
        if self.estado_actual == self.JUGANDO:
            # Actualizar jugador
            self.jugador.movimiento()
            
            # Actualizar sistemas
            self.game_manager.update(dt)
            self.map_manager.update(dt)
            
            # Limitar jugador al mapa actual
            if self.map_manager.current_map:
                mapa_rect = pygame.Rect(0, 0, self.map_manager.current_map.size[0], 
                                      self.map_manager.current_map.size[1])
                self.jugador.rect.clamp_ip(mapa_rect)
            
            # Actualizar cámara
            self.camara.x = self.jugador.rect.centerx - self.screen_size[0] // 2
            self.camara.y = self.jugador.rect.centery - self.screen_size[1] // 2
            
            # Limitar cámara
            if self.map_manager.current_map:
                mapa_rect = pygame.Rect(0, 0, self.map_manager.current_map.size[0], 
                                      self.map_manager.current_map.size[1])
                self.camara.x = max(0, min(self.camara.x, mapa_rect.width - self.screen_size[0]))
                self.camara.y = max(0, min(self.camara.y, mapa_rect.height - self.screen_size[1]))
            
            # Actualizar diálogo
            if self.dialogo_en_progreso and self.dialogo_activo:
                self.dialogo_activo.actualizar(dt)
                if not self.dialogo_activo.en_dialogo:
                    self.dialogo_en_progreso = False
    
    def draw(self):
        """Dibuja el juego."""
        if self.estado_actual == self.MENU:
            self.screen.blit(self.fondo_menu, (0, 0))
            
            # Mostrar instrucciones
            font = pygame.font.Font(None, 48)
            title_text = font.render("EL LADO OSCURO DEL CARRITO", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.screen_size[0]//2, 200))
            self.screen.blit(title_text, title_rect)
            
            instruction_font = pygame.font.Font(None, 32)
            instructions = [
                "Presiona ENTER para comenzar",
                "I - Abrir inventario",
                "M - Cambiar de mapa",
                "F1 - Mostrar información de depuración",
                "F2 - Alternar interfaces de sistemas"
            ]
            
            for i, instruction in enumerate(instructions):
                text = instruction_font.render(instruction, True, (200, 200, 200))
                text_rect = text.get_rect(center=(self.screen_size[0]//2, 300 + i * 40))
                self.screen.blit(text, text_rect)
        
        elif self.estado_actual == self.JUGANDO:
            # Dibujar mapa actual
            self.map_manager.draw(self.screen, (self.camara.x, self.camara.y))
            
            # Dibujar NPC y jugador
            self.screen.blit(self.vendedor.sprite, 
                           (self.vendedor.rect.x - self.camara.x, 
                            self.vendedor.rect.y - self.camara.y))
            self.jugador.dibujar(self.screen, self.camara)
            
            # Mostrar indicador de interacción
            if self.jugador.rect.colliderect(self.vendedor.rect.inflate(20, 20)):
                texto_e = self.fuente_interaccion.render("E", True, (255, 255, 255))
                e_x = self.vendedor.rect.centerx - texto_e.get_width() // 2 - self.camara.x
                e_y = self.vendedor.rect.top - 35 - self.camara.y
                self.screen.blit(texto_e, (e_x, e_y))
            
            # Dibujar diálogo
            if self.dialogo_en_progreso and self.dialogo_activo:
                self.dialogo_activo.dibujar(self.screen)
            
            # Aplicar efectos visuales del mundo
            if self.game_manager.world_state_manager:
                self.game_manager.world_state_manager.apply_world_effects(self.screen)
        
        # Dibujar interfaces de sistemas
        self.inventario.draw_ui(self.screen)
        self.game_manager.draw_system_uis(self.screen)
        self.game_manager.draw_debug_ui(self.screen)
        
        pygame.display.update()
    
    def run(self):
        """Bucle principal del juego."""
        print("=== EL LADO OSCURO DEL CARRITO - SISTEMA MEJORADO ===")
        print("Controles:")
        print("- ENTER: Comenzar juego")
        print("- ESC: Volver al menú")
        print("- I: Abrir/Cerrar inventario")
        print("- M: Cambiar de mapa")
        print("- F1: Mostrar información de depuración")
        print("- F2: Alternar interfaces de sistemas")
        print("- E: Interactuar con NPCs")
        print("- SPACE: Continuar diálogo")
        print("\nSistemas activos:")
        print("- Sistema de Equilibrio Interior")
        print("- Sistema de Dilemas Morales")
        print("- Sistema de Anuncios Manipuladores")
        print("- Sistema de Redención")
        print("- Sistema de Estado del Mundo")
        print("- Gestor de Mapas con State Machine")
        print("- Sistema de Inventario Refactorizado")
        print("\n¡Disfruta explorando las nuevas mecánicas!")
        
        while True:
            dt = self.handle_events()
            self.update(dt)
            self.draw()


def main():
    """Función principal."""
    try:
        game = EnhancedGame()
        game.run()
    except Exception as e:
        print(f"Error al ejecutar el juego: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
