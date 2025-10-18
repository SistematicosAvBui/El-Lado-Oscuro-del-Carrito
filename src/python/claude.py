import pygame
import sys
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
import random

# Inicializar Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (200, 200, 200)
GREEN = (50, 200, 50)
DARK_GREEN = (30, 120, 30)
RED = (200, 50, 50)
BLUE = (50, 100, 200)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (150, 50, 200)

class ItemType(Enum):
    CONSUMABLE = "consumable"
    REUSABLE = "reusable"
    RECYCLABLE = "recyclable"

@dataclass
class Item:
    name: str
    item_type: ItemType
    description: str
    ecological_value: int  # Valor ecológico (positivo = bueno)
    price: int
    durability: int = 100  # Para items reutilizables
    
class Quest:
    def __init__(self, title: str, description: str, reward_consciousness: int, objectives: Dict):
        self.title = title
        self.description = description
        self.reward_consciousness = reward_consciousness
        self.objectives = objectives
        self.completed = False
        self.progress = {key: 0 for key in objectives.keys()}
    
    def update_progress(self, objective_key: str, amount: int = 1):
        if objective_key in self.progress:
            self.progress[objective_key] += amount
            if self.progress[objective_key] >= self.objectives[objective_key]:
                self.progress[objective_key] = self.objectives[objective_key]
    
    def is_completed(self):
        return all(self.progress[k] >= self.objectives[k] for k in self.objectives.keys())

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 5
        self.color = BLUE
        self.inventory: List[Item] = []
        self.money = 100
        self.consciousness_level = 0  # Nivel de consciencia ecológica
        self.ecological_footprint = 100  # Huella ecológica (menor es mejor)
        
    def move(self, dx: int, dy: int, obstacles: List):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Verificar límites de pantalla
        if 0 <= new_x <= SCREEN_WIDTH - self.width:
            temp_rect = pygame.Rect(new_x, self.y, self.width, self.height)
            if not any(temp_rect.colliderect(obs.rect) for obs in obstacles):
                self.x = new_x
        
        if 0 <= new_y <= SCREEN_HEIGHT - self.height:
            temp_rect = pygame.Rect(self.x, new_y, self.width, self.height)
            if not any(temp_rect.colliderect(obs.rect) for obs in obstacles):
                self.y = new_y
    
    def add_item(self, item: Item):
        self.inventory.append(item)
        self.consciousness_level += item.ecological_value
        self.update_ecological_footprint()
    
    def remove_item(self, item: Item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.update_ecological_footprint()
    
    def update_ecological_footprint(self):
        # Calcular huella basada en items consumibles vs reutilizables
        consumables = sum(1 for item in self.inventory if item.item_type == ItemType.CONSUMABLE)
        reusables = sum(1 for item in self.inventory if item.item_type == ItemType.REUSABLE)
        self.ecological_footprint = max(0, 100 - (reusables * 5) + (consumables * 2) - self.consciousness_level)
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Sombra
        pygame.draw.rect(screen, DARK_GRAY, (self.x, self.y + self.height, self.width, 5))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class NPC:
    def __init__(self, x: int, y: int, name: str, dialogue: List[str], color: tuple):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.name = name
        self.dialogue = dialogue
        self.current_dialogue_index = 0
        self.color = color
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def interact(self):
        message = self.dialogue[self.current_dialogue_index]
        self.current_dialogue_index = (self.current_dialogue_index + 1) % len(self.dialogue)
        return message
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
        # Cabeza del NPC
        pygame.draw.circle(screen, self.color, (self.x + self.width//2, self.y - 10), 15)

class Obstacle:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple = DARK_GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

class Shop:
    def __init__(self):
        self.items_for_sale = [
            Item("Botella Plástica", ItemType.CONSUMABLE, 
                 "Contaminante, un solo uso", -5, 2),
            Item("Botella Reutilizable", ItemType.REUSABLE,
                 "¡Úsala mil veces!", 10, 25, 100),
            Item("Bolsa Plástica", ItemType.CONSUMABLE,
                 "Se rompe fácilmente", -3, 1),
            Item("Bolsa de Tela", ItemType.REUSABLE,
                 "Duradera y ecológica", 8, 15, 100),
            Item("Plato Desechable", ItemType.CONSUMABLE,
                 "Basura instantánea", -4, 3),
            Item("Plato Reutilizable", ItemType.REUSABLE,
                 "Para toda la vida", 7, 20, 100),
            Item("Material Reciclable", ItemType.RECYCLABLE,
                 "Conviértelo en algo nuevo", 15, 10),
        ]
        self.is_open = False
    
    def draw(self, screen: pygame.Surface, player: Player, font: pygame.font.Font):
        if not self.is_open:
            return
        
        # Fondo de la tienda
        shop_rect = pygame.Rect(150, 100, 900, 600)
        pygame.draw.rect(screen, WHITE, shop_rect)
        pygame.draw.rect(screen, BLACK, shop_rect, 3)
        
        # Título
        title = font.render("TIENDA CONSCIENTE", True, BLACK)
        screen.blit(title, (shop_rect.centerx - title.get_width()//2, 120))
        
        # Info del jugador
        info_font = pygame.font.Font(None, 28)
        money_text = info_font.render(f"Dinero: ${player.money}", True, GREEN)
        screen.blit(money_text, (170, 160))
        
        footprint_color = GREEN if player.ecological_footprint < 50 else ORANGE if player.ecological_footprint < 80 else RED
        footprint_text = info_font.render(f"Huella Ecológica: {player.ecological_footprint}", True, footprint_color)
        screen.blit(footprint_text, (170, 190))
        
        # Items en venta
        y_offset = 240
        for i, item in enumerate(self.items_for_sale):
            item_rect = pygame.Rect(170, y_offset, 860, 60)
            
            # Color según tipo
            if item.item_type == ItemType.CONSUMABLE:
                bg_color = (255, 200, 200)
            elif item.item_type == ItemType.REUSABLE:
                bg_color = (200, 255, 200)
            else:
                bg_color = (200, 200, 255)
            
            pygame.draw.rect(screen, bg_color, item_rect)
            pygame.draw.rect(screen, BLACK, item_rect, 2)
            
            # Nombre y precio
            name_text = info_font.render(f"{i+1}. {item.name} - ${item.price}", True, BLACK)
            screen.blit(name_text, (180, y_offset + 5))
            
            # Descripción
            desc_font = pygame.font.Font(None, 22)
            desc_text = desc_font.render(item.description, True, DARK_GRAY)
            screen.blit(desc_text, (180, y_offset + 32))
            
            # Valor ecológico
            eco_text = f"Valor Ecológico: {'+' if item.ecological_value >= 0 else ''}{item.ecological_value}"
            eco_color = GREEN if item.ecological_value > 0 else RED
            eco_render = desc_font.render(eco_text, True, eco_color)
            screen.blit(eco_render, (650, y_offset + 32))
            
            y_offset += 70
        
        # Instrucciones
        inst_text = info_font.render("Presiona 1-7 para comprar | ESC para cerrar", True, BLUE)
        screen.blit(inst_text, (shop_rect.centerx - inst_text.get_width()//2, 660))

class RecyclingCenter:
    def __init__(self):
        self.is_open = False
        self.recycled_items = []
    
    def recycle_item(self, item: Item, player: Player):
        if item.item_type == ItemType.RECYCLABLE or item.item_type == ItemType.CONSUMABLE:
            player.remove_item(item)
            reward = 5 + (item.ecological_value if item.ecological_value > 0 else 0)
            player.money += reward
            player.consciousness_level += 3
            self.recycled_items.append(item.name)
            return f"¡Reciclaste {item.name}! +${reward} +3 consciencia"
        return "Este item no se puede reciclar"
    
    def draw(self, screen: pygame.Surface, player: Player, font: pygame.font.Font):
        if not self.is_open:
            return
        
        center_rect = pygame.Rect(200, 150, 800, 500)
        pygame.draw.rect(screen, (230, 255, 230), center_rect)
        pygame.draw.rect(screen, DARK_GREEN, center_rect, 4)
        
        title = font.render("CENTRO DE RECICLAJE", True, DARK_GREEN)
        screen.blit(title, (center_rect.centerx - title.get_width()//2, 170))
        
        info_font = pygame.font.Font(None, 26)
        inst = info_font.render("Presiona el número del item para reciclarlo | ESC para cerrar", True, BLACK)
        screen.blit(inst, (center_rect.centerx - inst.get_width()//2, 210))
        
        # Mostrar inventario
        y_offset = 260
        recyclable_items = [item for item in player.inventory 
                          if item.item_type in [ItemType.RECYCLABLE, ItemType.CONSUMABLE]]
        
        if not recyclable_items:
            no_items = info_font.render("No tienes items reciclables", True, DARK_GRAY)
            screen.blit(no_items, (center_rect.centerx - no_items.get_width()//2, 350))
        else:
            for i, item in enumerate(recyclable_items[:8]):
                item_text = info_font.render(f"{i+1}. {item.name} - Valor: +${5 + max(0, item.ecological_value)}", True, BLACK)
                screen.blit(item_text, (230, y_offset))
                y_offset += 40

class QuestManager:
    def __init__(self):
        self.active_quests: List[Quest] = []
        self.completed_quests: List[Quest] = []
        
        # Crear misiones iniciales
        self.all_quests = [
            Quest("Consumidor Consciente", 
                  "Compra 3 items reutilizables en la tienda",
                  50, {"reusable_bought": 3}),
            Quest("Guerrero del Reciclaje",
                  "Recicla 5 items en el centro de reciclaje",
                  30, {"items_recycled": 5}),
            Quest("Reducción de Huella",
                  "Reduce tu huella ecológica a menos de 50",
                  40, {"footprint_reduced": 1}),
        ]
        
        self.active_quests.append(self.all_quests[0])
    
    def update_quest(self, objective_key: str, amount: int = 1):
        for quest in self.active_quests:
            quest.update_progress(objective_key, amount)
            if quest.is_completed() and not quest.completed:
                quest.completed = True
                return quest
        return None
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        quest_bg = pygame.Rect(10, 10, 350, 200)
        pygame.draw.rect(screen, (250, 250, 220), quest_bg)
        pygame.draw.rect(screen, BLACK, quest_bg, 2)
        
        title_font = pygame.font.Font(None, 30)
        title = title_font.render("MISIONES", True, BLACK)
        screen.blit(title, (20, 20))
        
        info_font = pygame.font.Font(None, 22)
        y_offset = 55
        
        for quest in self.active_quests[:3]:
            status = "✓" if quest.completed else "○"
            quest_title = info_font.render(f"{status} {quest.title}", True, GREEN if quest.completed else BLACK)
            screen.blit(quest_title, (20, y_offset))
            y_offset += 25
            
            for obj_key, obj_value in quest.objectives.items():
                progress = quest.progress[obj_key]
                progress_text = info_font.render(f"  {progress}/{obj_value}", True, DARK_GRAY)
                screen.blit(progress_text, (30, y_offset))
                y_offset += 22

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Consumismo Zero - RPG Ecológico")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Inicializar juego
        self.player = Player(100, 400)
        self.shop = Shop()
        self.recycling_center = RecyclingCenter()
        self.quest_manager = QuestManager()
        
        # NPCs con mensajes educativos
        self.npcs = [
            NPC(400, 200, "Eco-Mentor", [
                "¡Hola! Cada compra que haces tiene un impacto en el planeta.",
                "Los productos reutilizables cuestan más, pero duran años.",
                "¿Sabías que una botella plástica tarda 450 años en degradarse?",
                "La mejor compra es la que NO haces. ¿Realmente lo necesitas?"
            ], PURPLE),
            
            NPC(800, 300, "Activista Verde", [
                "El consumismo nos hace creer que necesitamos más de lo necesario.",
                "Reutilizar, reducir, reciclar. ¡En ese orden!",
                "Tu huella ecológica refleja tus decisiones diarias.",
                "Pequeños cambios crean grandes impactos."
            ], GREEN),
            
            NPC(600, 500, "Guardián del Planeta", [
                "Bienvenido al mundo post-consumista.",
                "Aquí valoramos la consciencia sobre la acumulación.",
                "Visita la tienda (T) para ver opciones conscientes.",
                "El centro de reciclaje (R) está al este."
            ], YELLOW)
        ]
        
        # Obstáculos (edificios, árboles, etc.)
        self.obstacles = [
            Obstacle(300, 100, 80, 80, (100, 70, 50)),  # Edificio
            Obstacle(700, 150, 100, 100, (100, 70, 50)),
            Obstacle(250, 450, 60, 60, DARK_GREEN),  # Árbol
            Obstacle(900, 400, 60, 60, DARK_GREEN),
            Obstacle(500, 600, 120, 40, GRAY),  # Banco
        ]
        
        # UI
        self.show_inventory = False
        self.show_stats = False
        self.dialogue_message = ""
        self.dialogue_timer = 0
        self.notification_message = ""
        self.notification_timer = 0
        
        # Contadores para misiones
        self.reusable_bought_count = 0
        self.items_recycled_count = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                # Abrir/cerrar interfaces
                if event.key == pygame.K_t:
                    self.shop.is_open = not self.shop.is_open
                
                if event.key == pygame.K_r:
                    self.recycling_center.is_open = not self.recycling_center.is_open
                
                if event.key == pygame.K_i:
                    self.show_inventory = not self.show_inventory
                
                if event.key == pygame.K_TAB:
                    self.show_stats = not self.show_stats
                
                if event.key == pygame.K_ESCAPE:
                    self.shop.is_open = False
                    self.recycling_center.is_open = False
                    self.show_inventory = False
                    self.show_stats = False
                
                # Interactuar con NPCs
                if event.key == pygame.K_SPACE:
                    self.interact_with_npcs()
                
                # Comprar en la tienda
                if self.shop.is_open:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, 
                                    pygame.K_5, pygame.K_6, pygame.K_7]:
                        index = event.key - pygame.K_1
                        self.buy_item(index)
                
                # Reciclar items
                if self.recycling_center.is_open:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                    pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8]:
                        index = event.key - pygame.K_1
                        recyclable_items = [item for item in self.player.inventory 
                                          if item.item_type in [ItemType.RECYCLABLE, ItemType.CONSUMABLE]]
                        if 0 <= index < len(recyclable_items):
                            message = self.recycling_center.recycle_item(recyclable_items[index], self.player)
                            self.show_notification(message)
                            self.items_recycled_count += 1
                            self.quest_manager.update_quest("items_recycled", 1)
                            
                            # Verificar misión de huella
                            if self.player.ecological_footprint < 50:
                                self.quest_manager.update_quest("footprint_reduced", 1)
    
    def buy_item(self, index: int):
        if 0 <= index < len(self.shop.items_for_sale):
            item = self.shop.items_for_sale[index]
            if self.player.money >= item.price:
                self.player.money -= item.price
                self.player.add_item(item)
                self.show_notification(f"Compraste: {item.name}")
                
                # Actualizar misión si es reutilizable
                if item.item_type == ItemType.REUSABLE:
                    self.reusable_bought_count += 1
                    completed_quest = self.quest_manager.update_quest("reusable_bought", 1)
                    if completed_quest:
                        self.show_notification(f"¡Misión completada! +{completed_quest.reward_consciousness} consciencia")
                        self.player.consciousness_level += completed_quest.reward_consciousness
            else:
                self.show_notification("¡No tienes suficiente dinero!")
    
    def interact_with_npcs(self):
        player_rect = self.player.get_rect()
        for npc in self.npcs:
            npc_rect = pygame.Rect(npc.x - 20, npc.y - 20, npc.width + 40, npc.height + 40)
            if player_rect.colliderect(npc_rect):
                self.dialogue_message = f"{npc.name}: {npc.interact()}"
                self.dialogue_timer = 300  # 5 segundos
                break
    
    def show_notification(self, message: str):
        self.notification_message = message
        self.notification_timer = 180  # 3 segundos
    
    def update(self):
        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        
        if not (self.shop.is_open or self.recycling_center.is_open):
            self.player.move(dx, dy, self.obstacles)
        
        # Actualizar timers
        if self.dialogue_timer > 0:
            self.dialogue_timer -= 1
        if self.notification_timer > 0:
            self.notification_timer -= 1
    
    def draw(self):
        # Fondo
        self.screen.fill((180, 220, 180))  # Verde claro
        
        # Dibujar obstáculos
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Dibujar NPCs
        for npc in self.npcs:
            npc.draw(self.screen)
            # Indicador de interacción
            player_rect = self.player.get_rect()
            npc_rect = pygame.Rect(npc.x - 20, npc.y - 20, npc.width + 40, npc.height + 40)
            if player_rect.colliderect(npc_rect):
                pygame.draw.circle(self.screen, WHITE, (npc.x + npc.width//2, npc.y - 30), 15)
                space_text = self.font_small.render("E", True, BLACK)
                self.screen.blit(space_text, (npc.x + npc.width//2 - 7, npc.y - 37))
        
        # Dibujar jugador
        self.player.draw(self.screen)
        
        # HUD Principal
        hud_rect = pygame.Rect(SCREEN_WIDTH - 260, 10, 250, 150)
        pygame.draw.rect(self.screen, (240, 240, 255), hud_rect)
        pygame.draw.rect(self.screen, BLACK, hud_rect, 2)
        
        money_text = self.font_small.render(f"Dinero: ${self.player.money}", True, BLACK)
        self.screen.blit(money_text, (SCREEN_WIDTH - 245, 20))
        
        consciousness_text = self.font_small.render(f"Consciencia: {self.player.consciousness_level}", True, BLUE)
        self.screen.blit(consciousness_text, (SCREEN_WIDTH - 245, 50))
        
        footprint_color = GREEN if self.player.ecological_footprint < 50 else ORANGE if self.player.ecological_footprint < 80 else RED
        footprint_text = self.font_small.render(f"Huella: {self.player.ecological_footprint}", True, footprint_color)
        self.screen.blit(footprint_text, (SCREEN_WIDTH - 245, 80))
        
        items_text = self.font_small.render(f"Items: {len(self.player.inventory)}", True, BLACK)
        self.screen.blit(items_text, (SCREEN_WIDTH - 245, 110))
        
        # Controles
        controls_y = SCREEN_HEIGHT - 80
        controls = [
            "WASD/Flechas: Mover | E: Interactuar",
            "T: Tienda | R: Reciclar | I: Inventario | TAB: Stats"
        ]
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, WHITE)
            bg_rect = pygame.Rect(10, controls_y + i * 30, text.get_width() + 20, 25)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
            self.screen.blit(text, (20, controls_y + 2 + i * 30))
        
        # Diálogo
        if self.dialogue_timer > 0:
            dialogue_rect = pygame.Rect(150, SCREEN_HEIGHT - 150, 900, 100)
            pygame.draw.rect(self.screen, WHITE, dialogue_rect)
            pygame.draw.rect(self.screen, BLACK, dialogue_rect, 3)
            
            # Dividir texto largo
            words = self.dialogue_message.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if self.font_medium.size(test_line)[0] < 860:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)
            
            y_offset = 0
            for line in lines[:3]:
                text = self.font_medium.render(line, True, BLACK)
                self.screen.blit(text, (160, SCREEN_HEIGHT - 140 + y_offset))
                y_offset += 30
        
        # Notificación
        if self.notification_timer > 0:
            notif_text = self.font_medium.render(self.notification_message, True, WHITE)
            notif_rect = pygame.Rect(SCREEN_WIDTH//2 - notif_text.get_width()//2 - 20,
                                     50, notif_text.get_width() + 40, 50)
            pygame.draw.rect(self.screen, (50, 50, 50, 200), notif_rect)
            self.screen.blit(notif_text, (SCREEN_WIDTH//2 - notif_text.get_width()//2, 60))
        
        # Dibujar interfaces
        self.quest_manager.draw(self.screen, self.font_medium)
        self.shop.draw(self.screen, self.player, self.font_large)
        self.recycling_center.draw(self.screen, self.player, self.font_large)
        
        # Inventario
        if self.show_inventory:
            inv_rect = pygame.Rect(300, 150, 600, 500)
            pygame.draw.rect(self.screen, WHITE, inv_rect)
            pygame.draw.rect(self.screen, BLACK, inv_rect, 3)
            
            title = self.font_large.render("INVENTARIO", True, BLACK)
            self.screen.blit(title, (inv_rect.centerx - title.get_width()//2, 170))
            
            if not self.player.inventory:
                empty_text = self.font_medium.render("Inventario vacío", True, DARK_GRAY)
                self.screen.blit(empty_text, (inv_rect.centerx - empty_text.get_width()//2, 350))
            else:
                y_offset = 230
                for item in self.player.inventory[:10]:
                    item_color = RED if item.item_type == ItemType.CONSUMABLE else GREEN
                    item_text = self.font_small.render(f"• {item.name} ({item.item_type.value})", True, item_color)
                    self.screen.blit(item_text, (320, y_offset))
                    y_offset += 35
        
        # Estadísticas
        if self.show_stats:
            stats_rect = pygame.Rect(250, 100, 700, 600)
            pygame.draw.rect(self.screen, (255, 250, 240), stats_rect)
            pygame.draw.rect(self.screen, BLACK, stats_rect, 3)
            
            title = self.font_large.render("ESTADÍSTICAS", True, BLACK)
            self.screen.blit(title, (stats_rect.centerx - title.get_width()//2, 120))
            
            y_offset = 200
            stats_info = [
                f"Nivel de Consciencia: {self.player.consciousness_level}",
                f"Huella Ecológica: {self.player.ecological_footprint}",
                f"Dinero Total: ${self.player.money}",
                f"Items en Inventario: {len(self.player.inventory)}",
                f"Items Reutilizables: {sum(1 for i in self.player.inventory if i.item_type == ItemType.REUSABLE)}",
                f"Items Consumibles: {sum(1 for i in self.player.inventory if i.item_type == ItemType.CONSUMABLE)}",
                f"Items Reciclados: {self.items_recycled_count}",
                f"Compras Conscientes: {self.reusable_bought_count}",
            ]
            
            for stat in stats_info:
                text = self.font_medium.render(stat, True, BLACK)
                self.screen.blit(text, (270, y_offset))
                y_offset += 45
            
            # Consejos
            y_offset += 30
            advice_title = self.font_medium.render("CONSEJOS:", True, BLUE)
            self.screen.blit(advice_title, (270, y_offset))
            y_offset += 35
            
            advice_font = pygame.font.Font(None, 24)
            if self.player.ecological_footprint > 80:
                advice = "Tu huella es alta. Compra más items reutilizables."
                color = RED
            elif self.player.ecological_footprint > 50:
                advice = "Vas bien. Sigue reciclando y reduciendo consumo."
                color = ORANGE
            else:
                advice = "¡Excelente! Eres un consumidor consciente."
                color = GREEN
            
            advice_text = advice_font.render(advice, True, color)
            self.screen.blit(advice_text, (270, y_offset))
        
        pygame.display.flip()
    
    def run(self):
        """Ciclo principal del juego"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Punto de entrada del programa
if __name__ == "__main__":
    game = Game()
    game.run()