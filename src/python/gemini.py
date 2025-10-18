import pygame
import sys

# --- Constantes del Juego ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 32 # Tamaño de los "tiles" o bloques, también para nuestros rectángulos

# Colores (en formato RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
BLUE = (50, 50, 200)
RED = (200, 50, 50)    # Color para el jugador
GREY = (100, 100, 100) # Color para NPCs u otros objetos

# Estado del Juego
GAME_STATE = {
    'RUNNING': 0,
    'MENU': 1,
    'INVENTORY': 2,
    'DIALOGUE': 3
}

# ----------------------------------------------------
## Clase Base: GameObject
# ----------------------------------------------------
class GameObject:
    """Clase base para cualquier objeto en el juego con posición y dibujo."""
    def __init__(self, x, y, color):
        self.color = color
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE) # Un rectángulo de TILE_SIZE
        self.x = x
        self.y = y

    def draw(self, surface):
        """Dibuja el objeto como un rectángulo de color en la superficie dada."""
        pygame.draw.rect(surface, self.color, self.rect)

# ----------------------------------------------------
## Clase: Player (Jugador)
# ----------------------------------------------------
class Player(GameObject):
    """Maneja el personaje principal, sus estadísticas y su inventario."""
    def __init__(self, x, y):
        super().__init__(x, y, RED) # El jugador será un rectángulo rojo
        self.speed = 4
        self.inventory = Inventory()
        self.influence_green = 0
        self.points_sustainability = 100

    def move(self, dx, dy):
        """Mueve al jugador y actualiza su rectángulo."""
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.topleft = (int(self.x), int(self.y)) # Asegurarse de que las coordenadas sean enteras
        # TODO: Implementar lógica de colisión con el mapa y NPCs

    def update(self):
        """Maneja la entrada del teclado para el movimiento."""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        if dx != 0 and dy != 0:
            factor = 0.707
            self.move(dx * factor, dy * factor)
        else:
            self.move(dx, dy)
    
    def interact(self, target):
        """Permite la interacción con NPCs o estaciones de trabajo (Taller)."""
        print(f"Interactuando con {target.__class__.__name__}")

# ----------------------------------------------------
## Clase: NPC (Personaje No Jugable)
# ----------------------------------------------------
class NPC(GameObject):
    """Un NPC simple, representado por un rectángulo."""
    def __init__(self, x, y, name="NPC"):
        super().__init__(x, y, GREY) # NPCs serán rectángulos grises
        self.name = name
        self.dialogue = ["Hola, humano. ¡Menos consumir y más producir!", "El reciclaje es el futuro."]
        self.current_dialogue_idx = 0

    def start_dialogue(self):
        """Inicia el diálogo con el NPC."""
        if self.dialogue:
            print(f"{self.name}: {self.dialogue[self.current_dialogue_idx]}")
            self.current_dialogue_idx = (self.current_dialogue_idx + 1) % len(self.dialogue)
            return self.dialogue[self.current_dialogue_idx -1] # Retorna la línea actual para la UI
        return ""

# ----------------------------------------------------
## Clase: Inventory (Inventario)
# ----------------------------------------------------
class Inventory:
    """Maneja la colección de ítems y componentes del jugador."""
    def __init__(self):
        self.items = []     # Objetos de Equipment o Item
        self.components = {} # Componentes base (ej: {'Metal Reciclado': 5, 'Plástico': 12})
        self.max_size = 20

    def add_item(self, item):
        """Añade un ítem al inventario si hay espacio."""
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        return False

# ----------------------------------------------------
## Clase: Game (Motor Principal)
# ----------------------------------------------------
class Game:
    """Clase principal que contiene el bucle del juego y gestiona los objetos."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Great Refactor - Anti-Consumism RPG")
        self.clock = pygame.time.Clock()
        
        self.state = GAME_STATE['RUNNING']
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Añadir un NPC de prueba
        self.npcs = [NPC(SCREEN_WIDTH // 2 + TILE_SIZE * 3, SCREEN_HEIGHT // 2, "El Reciclador")]
        
        # Intentar cargar una fuente personalizada si existe, si no, usa una por defecto
        try:
            self.font = pygame.font.Font('assets/PixelFont.ttf', 24)
            self.small_font = pygame.font.Font('assets/PixelFont.ttf', 18)
        except:
            self.font = pygame.font.SysFont('Arial', 24)
            self.small_font = pygame.font.SysFont('Arial', 18)

        # Diálogo actual para mostrar en pantalla
        self.current_dialogue_text = ""
        self.dialogue_speaker = ""

    def handle_events(self):
        """Maneja todos los eventos de entrada (teclado, ratón)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                
                if event.key == pygame.K_i:
                    if self.state == GAME_STATE['RUNNING']:
                        self.state = GAME_STATE['INVENTORY']
                    elif self.state == GAME_STATE['INVENTORY']:
                        self.state = GAME_STATE['RUNNING']
                
                if event.key == pygame.K_e:
                    if self.state == GAME_STATE['RUNNING']:
                        # Comprobar si hay un NPC cerca para interactuar
                        for npc in self.npcs:
                            if self.player.rect.colliderect(npc.rect.inflate(TILE_SIZE, TILE_SIZE)): # Un poco de margen para la interacción
                                self.player.interact(npc)
                                self.current_dialogue_text = npc.start_dialogue()
                                self.dialogue_speaker = npc.name
                                self.state = GAME_STATE['DIALOGUE']
                                break
                    elif self.state == GAME_STATE['DIALOGUE']:
                        # Al presionar E de nuevo, avanza el diálogo o lo cierra
                        # Por ahora, simplemente cierra el diálogo
                        self.current_dialogue_text = ""
                        self.dialogue_speaker = ""
                        self.state = GAME_STATE['RUNNING']

    def update(self):
        """Actualiza la lógica del juego (movimiento, colisiones, etc.)."""
        if self.state == GAME_STATE['RUNNING']:
            self.player.update()
        # Los NPCs, mapa, etc., solo se actualizan si el juego está corriendo

    def draw(self):
        """Dibuja todos los elementos en pantalla."""
        self.screen.fill(BLUE)
        
        self.player.draw(self.screen)
        
        for npc in self.npcs:
            npc.draw(self.screen)
        
        self.draw_hud()

        if self.state == GAME_STATE['INVENTORY']:
            self.draw_inventory_menu()
        
        if self.state == GAME_STATE['DIALOGUE']:
            self.draw_dialogue_box()
        
        pygame.display.flip()

    def draw_hud(self):
        """Dibuja la información crucial en pantalla (HUD)."""
        ps_text = self.font.render(f"PS: {self.player.points_sustainability}", True, WHITE)
        inf_text = self.font.render(f"Influencia: {self.player.influence_green}", True, WHITE)
        
        self.screen.blit(ps_text, (10, 10))
        self.screen.blit(inf_text, (10, 40))

    def draw_inventory_menu(self):
        """Dibuja la interfaz del inventario."""
        s = pygame.Surface((SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
        s.set_alpha(200)
        s.fill(BLACK)
        self.screen.blit(s, (50, 50))

        title_text = self.font.render("INVENTARIO DE REUTILIZACIÓN (I)", True, GREEN)
        self.screen.blit(title_text, (60, 60))
        
        comp_y = 100
        comp_title = self.small_font.render("Componentes:", True, WHITE)
        self.screen.blit(comp_title, (60, comp_y))
        
        for name, count in self.player.inventory.components.items():
            comp_y += 25 # Espacio más pequeño para la fuente pequeña
            text = self.small_font.render(f"- {name}: {count}", True, WHITE)
            self.screen.blit(text, (80, comp_y))

    def draw_dialogue_box(self):
        """Dibuja una caja de diálogo en la parte inferior de la pantalla."""
        box_height = 120
        dialogue_rect = pygame.Rect(0, SCREEN_HEIGHT - box_height, SCREEN_WIDTH, box_height)
        
        s = pygame.Surface((dialogue_rect.width, dialogue_rect.height))
        s.set_alpha(180)
        s.fill(BLACK)
        self.screen.blit(s, dialogue_rect)

        pygame.draw.rect(self.screen, WHITE, dialogue_rect, 3) # Borde blanco

        # Texto del orador
        speaker_surf = self.small_font.render(f"{self.dialogue_speaker}:", True, GREEN)
        self.screen.blit(speaker_surf, (dialogue_rect.x + 10, dialogue_rect.y + 10))

        # Texto del diálogo
        dialogue_surf = self.small_font.render(self.current_dialogue_text, True, WHITE)
        self.screen.blit(dialogue_surf, (dialogue_rect.x + 15, dialogue_rect.y + 40))

        # Indicación para continuar
        continue_text = self.small_font.render("[Presiona 'E' para continuar]", True, GREY)
        self.screen.blit(continue_text, (dialogue_rect.x + dialogue_rect.width - continue_text.get_width() - 10, dialogue_rect.y + box_height - continue_text.get_height() - 10))


    def run(self):
        """Bucle principal del juego."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def quit_game(self):
        """Cierra PyGame y sale del sistema."""
        pygame.quit()
        sys.exit()

# --- Punto de entrada principal ---
if __name__ == '__main__':
    # Creación de un inventario mock para el jugador
    player_mock_inventory = Inventory()
    player_mock_inventory.components = {
        'Plástico Reciclado': 5, 
        'Metal Recuperado': 12,
        'Circuitos Viejos': 3
    }
    
    g = Game()
    g.player.inventory = player_mock_inventory # Asignación del inventario mock al jugador
    
    g.run()