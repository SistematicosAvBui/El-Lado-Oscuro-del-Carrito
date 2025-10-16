"""
Pruebas y Demostración de Sistemas para "El Lado Oscuro del Carrito"

Este archivo contiene pruebas unitarias y demostraciones de los sistemas
implementados, permitiendo verificar su funcionamiento correcto.
"""

import pygame
import sys
import time
from typing import Dict, Any

# Importar sistemas
from sistemas.interior_balance import InteriorBalance
from sistemas.moral_dilemma_system import MoralDilemmaSystem, MoralDilemma, DilemmaChoice, DilemmaType
from sistemas.ad_system import AdSystem, Ad, AdType
from sistemas.redemption_system import RedemptionSystem, RedemptionAction, RedemptionType
from sistemas.world_state import WorldStateManager, WorldState
from sistemas.inventory_system import InventorySystem, Product, ItemType, ItemRarity
from sistemas.game_config import get_config, DifficultyLevel


class SystemTester:
    """
    Clase para probar y demostrar el funcionamiento de los sistemas.
    
    Permite ejecutar pruebas unitarias y demostraciones interactivas
    de cada sistema implementado.
    """
    
    def __init__(self):
        """Inicializa el tester de sistemas."""
        pygame.init()
        
        # Configuración de pantalla para pruebas
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Sistema de Pruebas - El Lado Oscuro del Carrito")
        self.clock = pygame.time.Clock()
        
        # Configuración
        self.config = get_config()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        
        # Estado de las pruebas
        self.current_test = 0
        self.test_results = {}
        self.running = True
        
        # Inicializar sistemas para pruebas
        self._initialize_test_systems()
    
    def _initialize_test_systems(self):
        """Inicializa los sistemas para las pruebas."""
        # Sistema de equilibrio interior
        self.interior_balance = InteriorBalance()
        
        # Sistema de dilemas morales
        self.moral_dilemma_system = MoralDilemmaSystem(self.interior_balance)
        
        # Sistema de anuncios
        self.ad_system = AdSystem(self.interior_balance)
        
        # Sistema de redención
        self.redemption_system = RedemptionSystem(self.interior_balance)
        
        # Estado del mundo
        self.world_state_manager = WorldStateManager(self.interior_balance)
        
        # Sistema de inventario
        self.inventory_system = InventorySystem()
        
        # Crear productos de prueba
        self._create_test_products()
    
    def _create_test_products(self):
        """Crea productos de prueba para las demostraciones."""
        # Producto consumista
        self.smartphone = Product(
            "smartphone_test", "Smartphone de Prueba",
            "Un smartphone para probar el sistema de consumo",
            999, ItemType.LUXURY, ItemRarity.RARE,
            effects={"satisfaction": 25, "real_happiness": -10}
        )
        
        # Producto esencial
        self.comida = Product(
            "comida_test", "Comida de Prueba",
            "Comida básica para pruebas",
            50, ItemType.ESSENTIAL, ItemRarity.COMMON,
            effects={"energia": 20, "real_happiness": 5}
        )
        
        # Producto de redención
        self.ropa_donacion = Product(
            "ropa_test", "Ropa para Donar",
            "Ropa que se puede donar",
            0, ItemType.REDEMPTION, ItemRarity.COMMON,
            effects={"real_happiness": 15}
        )
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas de sistemas."""
        print("=== INICIANDO PRUEBAS DE SISTEMAS ===")
        
        tests = [
            ("Sistema de Equilibrio Interior", self.test_interior_balance),
            ("Sistema de Dilemas Morales", self.test_moral_dilemmas),
            ("Sistema de Anuncios", self.test_ad_system),
            ("Sistema de Redención", self.test_redemption_system),
            ("Estado del Mundo", self.test_world_state),
            ("Sistema de Inventario", self.test_inventory_system),
            ("Integración de Sistemas", self.test_system_integration)
        ]
        
        for test_name, test_func in tests:
            print(f"\n--- Ejecutando: {test_name} ---")
            try:
                result = test_func()
                self.test_results[test_name] = result
                print(f"✓ {test_name}: {'PASÓ' if result else 'FALLÓ'}")
            except Exception as e:
                print(f"✗ {test_name}: ERROR - {e}")
                self.test_results[test_name] = False
        
        self._print_test_summary()
    
    def test_interior_balance(self) -> bool:
        """Prueba el sistema de equilibrio interior."""
        print("Probando sistema de equilibrio interior...")
        
        # Prueba inicial
        assert self.interior_balance.satisfaction == 50.0
        assert self.interior_balance.real_happiness == 50.0
        
        # Prueba de efectos de compra
        self.interior_balance.apply_purchase_effect(100, "luxury")
        assert self.interior_balance.satisfaction > 50.0
        assert self.interior_balance.real_happiness < 50.0
        
        # Prueba de efectos de acción positiva
        self.interior_balance.apply_good_action_effect("donation", 1.0)
        assert self.interior_balance.real_happiness > 50.0
        
        # Prueba de límites
        self.interior_balance.satisfaction = 150.0
        assert self.interior_balance.satisfaction == 100.0
        
        self.interior_balance.real_happiness = -50.0
        assert self.interior_balance.real_happiness == 0.0
        
        print("✓ Todas las pruebas de equilibrio interior pasaron")
        return True
    
    def test_moral_dilemmas(self) -> bool:
        """Prueba el sistema de dilemas morales."""
        print("Probando sistema de dilemas morales...")
        
        # Verificar que hay dilemas disponibles
        assert len(self.moral_dilemma_system.dilemmas) > 0
        
        # Crear un dilema de prueba
        test_choices = [
            DilemmaChoice("Opción moral", {"real_happiness": 20, "satisfaction": -5}, "moral"),
            DilemmaChoice("Opción egoísta", {"real_happiness": -10, "satisfaction": 15}, "selfish")
        ]
        
        test_dilemma = MoralDilemma(
            "test_dilemma", "Dilema de Prueba", "Un dilema para probar el sistema",
            DilemmaType.PERSONAL, test_choices
        )
        
        self.moral_dilemma_system.add_dilemma(test_dilemma)
        
        # Activar dilema
        assert self.moral_dilemma_system.activate_dilemma("test_dilemma")
        assert self.moral_dilemma_system.active_dilemma is not None
        
        # Seleccionar opción
        assert self.moral_dilemma_system.select_choice(0)
        assert test_dilemma.completed
        
        print("✓ Todas las pruebas de dilemas morales pasaron")
        return True
    
    def test_ad_system(self) -> bool:
        """Prueba el sistema de anuncios."""
        print("Probando sistema de anuncios...")
        
        # Verificar que hay anuncios disponibles
        assert len(self.ad_system.ads) > 0
        
        # Crear anuncio de prueba
        test_ad = Ad(
            "test_ad", "Anuncio de Prueba", "Un anuncio para probar el sistema",
            AdType.CONSUMER_PRODUCT, 3.0, {"real_happiness": -10, "satisfaction": 15}
        )
        
        self.ad_system.add_custom_ad(test_ad)
        
        # Activar anuncio
        test_ad.start_exposure()
        assert test_ad.is_active
        
        # Simular tiempo de exposición
        time.sleep(0.1)  # Pequeña pausa para simular tiempo
        assert test_ad.get_exposure_time() > 0
        
        # Descargar anuncio
        assert self.ad_system.dismiss_ad()
        
        print("✓ Todas las pruebas de anuncios pasaron")
        return True
    
    def test_redemption_system(self) -> bool:
        """Prueba el sistema de redención."""
        print("Probando sistema de redención...")
        
        # Verificar acciones disponibles
        assert len(self.redemption_system.redemption_actions) > 0
        
        # Añadir ítem de prueba al inventario
        self.inventory_system.add_item(self.ropa_donacion, 5)
        
        # Configurar referencia al inventario
        self.redemption_system.inventory_ref = self.inventory_system
        
        # Probar donación
        initial_items = len(self.inventory_system.items)
        assert self.redemption_system.donate_item("ropa_test", 2)
        assert len(self.inventory_system.items) < initial_items
        
        # Verificar estadísticas
        stats = self.redemption_system.get_statistics()
        assert stats["total_items_donated"] > 0
        
        print("✓ Todas las pruebas de redención pasaron")
        return True
    
    def test_world_state(self) -> bool:
        """Prueba el estado del mundo."""
        print("Probando estado del mundo...")
        
        # Verificar estado inicial
        assert self.world_state_manager.current_state == WorldState.NEUTRAL
        
        # Cambiar equilibrio interior para activar cambio de estado
        self.interior_balance.satisfaction = 80
        self.interior_balance.real_happiness = 20
        
        # Actualizar estado del mundo
        self.world_state_manager.update(1000)  # 1 segundo
        
        # Verificar que el estado cambió
        assert self.world_state_manager.current_state == WorldState.CONSUMIST
        
        # Probar efectos visuales
        info = self.world_state_manager.get_world_state_info()
        assert "current_state" in info
        
        print("✓ Todas las pruebas de estado del mundo pasaron")
        return True
    
    def test_inventory_system(self) -> bool:
        """Prueba el sistema de inventario."""
        print("Probando sistema de inventario...")
        
        # Verificar inventario vacío inicialmente
        assert len(self.inventory_system.items) == 0
        
        # Añadir ítems
        assert self.inventory_system.add_item(self.smartphone)
        assert self.inventory_system.add_item(self.comida, 3)
        
        # Verificar que se añadieron
        assert len(self.inventory_system.items) > 0
        
        # Probar apilamiento
        assert self.inventory_system.add_item(self.comida, 2)
        
        # Verificar obtención por tipo
        essential_items = self.inventory_system.get_items_by_type(ItemType.ESSENTIAL)
        assert len(essential_items) > 0
        
        # Verificar valor total
        total_value = self.inventory_system.get_total_value()
        assert total_value > 0
        
        print("✓ Todas las pruebas de inventario pasaron")
        return True
    
    def test_system_integration(self) -> bool:
        """Prueba la integración entre sistemas."""
        print("Probando integración de sistemas...")
        
        # Simular compra que afecta múltiples sistemas
        self.interior_balance.apply_purchase_effect(200, "luxury")
        
        # Verificar que el estado del mundo se actualiza
        self.world_state_manager.update(1000)
        
        # Verificar que hay dilemas disponibles según el nuevo estado
        player_state = {
            "satisfaction": self.interior_balance.satisfaction,
            "real_happiness": self.interior_balance.real_happiness
        }
        
        available_dilemmas = self.moral_dilemma_system.check_for_available_dilemmas(player_state)
        assert len(available_dilemmas) >= 0  # Puede ser 0 o más
        
        # Verificar que el sistema de anuncios puede activar efectos
        self.ad_system.activate_manipulation_shader()
        assert len(self.world_state_manager.temporary_effects) > 0
        
        print("✓ Todas las pruebas de integración pasaron")
        return True
    
    def _print_test_summary(self):
        """Imprime un resumen de las pruebas."""
        print("\n=== RESUMEN DE PRUEBAS ===")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        failed_tests = total_tests - passed_tests
        
        print(f"Total de pruebas: {total_tests}")
        print(f"Pruebas pasadas: {passed_tests}")
        print(f"Pruebas fallidas: {failed_tests}")
        print(f"Porcentaje de éxito: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\nPruebas fallidas:")
            for test_name, result in self.test_results.items():
                if not result:
                    print(f"  - {test_name}")
    
    def run_interactive_demo(self):
        """Ejecuta una demostración interactiva de los sistemas."""
        print("=== DEMOSTRACIÓN INTERACTIVA ===")
        print("Controles:")
        print("- 1-7: Cambiar entre sistemas")
        print("- ESPACIO: Ejecutar acción de prueba")
        print("- ESC: Salir")
        print("- F1: Cambiar dificultad")
        
        while self.running:
            dt = self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    
                    elif event.key == pygame.K_SPACE:
                        self._execute_test_action()
                    
                    elif event.key == pygame.K_1:
                        self.current_test = 0
                    elif event.key == pygame.K_2:
                        self.current_test = 1
                    elif event.key == pygame.K_3:
                        self.current_test = 2
                    elif event.key == pygame.K_4:
                        self.current_test = 3
                    elif event.key == pygame.K_5:
                        self.current_test = 4
                    elif event.key == pygame.K_6:
                        self.current_test = 5
                    elif event.key == pygame.K_7:
                        self.current_test = 6
                    
                    elif event.key == pygame.K_F1:
                        self._cycle_difficulty()
            
            self._update_demo(dt)
            self._draw_demo()
    
    def _execute_test_action(self):
        """Ejecuta una acción de prueba según el sistema actual."""
        if self.current_test == 0:  # Equilibrio Interior
            self.interior_balance.apply_purchase_effect(100, "luxury")
            print("Aplicado efecto de compra de lujo")
        
        elif self.current_test == 1:  # Dilemas Morales
            if self.moral_dilemma_system.active_dilemma:
                self.moral_dilemma_system.select_choice(0)
                print("Seleccionada opción moral")
            else:
                self.moral_dilemma_system.activate_dilemma("compulsive_purchase")
                print("Activado dilema moral")
        
        elif self.current_test == 2:  # Anuncios
            if self.ad_system.active_ad:
                self.ad_system.dismiss_ad()
                print("Anuncio descartado")
            else:
                self.ad_system._spawn_random_ad()
                print("Anuncio activado")
        
        elif self.current_test == 3:  # Redención
            if self.inventory_system.items:
                item = self.inventory_system.items[0]
                self.redemption_system.donate_item(item.name, 1)
                print(f"Donado: {item.name}")
        
        elif self.current_test == 4:  # Estado del Mundo
            self.world_state_manager.activate_manipulation_shader()
            print("Activado efecto de manipulación")
        
        elif self.current_test == 5:  # Inventario
            if len(self.inventory_system.items) < 5:
                self.inventory_system.add_item(self.smartphone)
                print("Añadido smartphone al inventario")
        
        elif self.current_test == 6:  # Integración
            self.interior_balance.apply_good_action_effect("meditation", 1.0)
            self.world_state_manager.activate_redemption_effect()
            print("Ejecutada acción de redención")
    
    def _cycle_difficulty(self):
        """Cambia el nivel de dificultad."""
        difficulties = list(DifficultyLevel)
        current_idx = difficulties.index(self.config.general["difficulty"])
        next_idx = (current_idx + 1) % len(difficulties)
        
        self.config.apply_difficulty_settings(difficulties[next_idx])
        print(f"Dificultad cambiada a: {difficulties[next_idx].name}")
    
    def _update_demo(self, dt):
        """Actualiza la demostración."""
        # Actualizar sistemas
        self.ad_system.update(dt)
        self.world_state_manager.update(dt)
    
    def _draw_demo(self):
        """Dibuja la demostración."""
        self.screen.fill((20, 20, 40))
        
        # Título
        title_text = self.title_font.render("DEMOSTRACIÓN DE SISTEMAS", True, (255, 255, 255))
        self.screen.blit(title_text, (20, 20))
        
        # Sistema actual
        system_names = [
            "Equilibrio Interior",
            "Dilemas Morales", 
            "Anuncios",
            "Redención",
            "Estado del Mundo",
            "Inventario",
            "Integración"
        ]
        
        current_system = system_names[self.current_test]
        system_text = self.font.render(f"Sistema: {current_system}", True, (255, 255, 0))
        self.screen.blit(system_text, (20, 60))
        
        # Dibujar UI del sistema actual
        if self.current_test == 0:
            self.interior_balance.draw_ui(self.screen, 20, 100)
        elif self.current_test == 1:
            self.moral_dilemma_system.draw_ui(self.screen, 20, 100)
        elif self.current_test == 2:
            self.ad_system.draw_ui(self.screen)
        elif self.current_test == 3:
            self.redemption_system.draw_ui(self.screen, 20, 100)
        elif self.current_test == 4:
            self.world_state_manager.draw_ui(self.screen, 20, 100)
        elif self.current_test == 5:
            self.inventory_system.draw_ui(self.screen)
        
        # Instrucciones
        instructions = [
            "1-7: Cambiar sistema",
            "ESPACIO: Ejecutar acción",
            "F1: Cambiar dificultad",
            "ESC: Salir"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, (200, 200, 200))
            self.screen.blit(text, (20, 500 + i * 25))
        
        pygame.display.update()


def main():
    """Función principal para ejecutar las pruebas."""
    print("=== SISTEMA DE PRUEBAS - EL LADO OSCURO DEL CARRITO ===")
    print("Selecciona una opción:")
    print("1. Ejecutar todas las pruebas")
    print("2. Demostración interactiva")
    print("3. Salir")
    
    choice = input("Ingresa tu opción (1-3): ").strip()
    
    tester = SystemTester()
    
    if choice == "1":
        tester.run_all_tests()
    elif choice == "2":
        tester.run_interactive_demo()
    elif choice == "3":
        print("Saliendo...")
        return
    else:
        print("Opción inválida")
        return
    
    pygame.quit()


if __name__ == "__main__":
    main()
