import pygame
from compilados_py.Release import personaje as per  # tu binding en C++

class Personajes(per.Personaje):
    def __init__(self, eje_x, eje_y, velocidad, ancho, alto, sprite_path=None):
        # Personaje C++ requiere (movimiento, dinero)
        super().__init__(0, 100)
        self.eje_x = eje_x
        self.eje_y = eje_y
        self.velocidad = velocidad
        self.ancho = ancho
        self.alto = alto

        # Si pasamos ruta, cargamos el sprite
        if sprite_path:
            imagen = pygame.image.load(sprite_path).convert_alpha()
            self.image = pygame.transform.scale(imagen, (ancho, alto))
        else:
            self.image = None

    def rect(self):
        return pygame.Rect(int(self.eje_x), int(self.eje_y), self.ancho, self.alto)

    def draw(self, pantalla, color=(200, 0, 0)):
        if self.image:
            pantalla.blit(self.image, (self.eje_x, self.eje_y))
        else:
            pygame.draw.rect(pantalla, color, self.rect())


class Protagonista(Personajes):
    def __init__(self, eje_x, eje_y, velocidad, ancho, alto, sprite_path=None):
        super().__init__(eje_x, eje_y, velocidad, ancho, alto, sprite_path)

    def movimiento_jugador(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            self.eje_y -= self.velocidad
        if teclas[pygame.K_s]:
            self.eje_y += self.velocidad
        if teclas[pygame.K_a]:
            self.eje_x -= self.velocidad
        if teclas[pygame.K_d]:
            self.eje_x += self.velocidad

    def interaccion(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_e]:
            print("Interacción: tecla E pulsada")

    def economia(self, cantidad):
        print(f"Gastando {cantidad}...")
        self.gasto(cantidad)  # método expuesto desde C++
        print(f"Dinero ahora: {self.dinero}")


class NPC(Personajes):
    def __init__(self, eje_x, eje_y, velocidad, ancho, alto, sprite_path=None):
        super().__init__(eje_x, eje_y, velocidad, ancho, alto, sprite_path)

    def seguir(self, jugador):
        dx = jugador.eje_x - self.eje_x
        dy = jugador.eje_y - self.eje_y
        distancia = (dx**2 + dy**2) ** 0.5
        if distancia > 0:
            self.eje_x += self.velocidad * dx / distancia
            self.eje_y += self.velocidad * dy / distancia

    def interaccion(self):
        print("NPC: Te estoy siguiendo 👀")


