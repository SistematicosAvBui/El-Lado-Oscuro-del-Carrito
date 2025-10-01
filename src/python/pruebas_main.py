'''import pygame
from personaje2 import Protagonista, NPC

class Juego():
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("El Lado Oscuro del Carrito")
        self.tasa_f = pygame.time.Clock()

        # Fondos
        self.fondo_menu = pygame.image.load("assets/imagen_fondo_principal2.png")
        self.fondo_menu = pygame.transform.scale(self.fondo_menu, (1200, 600))

        self.fondo_nivel = pygame.image.load("assets/imagen_nivel.jpg").convert()
        self.fondo_nivel = pygame.transform.scale(self.fondo_nivel, (1200, 600))

        # Personajes con sprites (si no existen las imágenes, se verán como rectángulos)
        self.jugador = Protagonista(
            100, 100, 3, 40, 60, "assets/imagen_jugador.png"
        )
        self.npc = NPC(
            400, 300, 2, 40, 60, "assets/imagen_prepuncho.png"
        )

    def ejecucion_juego(self):
        MENU = "menu"
        JUGANDO = "jugando"
        estado = MENU

        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

                if estado == MENU:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                        estado = JUGANDO
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 500 <= x <= 650 and 450 <= y <= 520:
                            estado = JUGANDO

            if estado == MENU:
                self.pantalla.fill((0, 0, 0))
                self.pantalla.blit(self.fondo_menu, (0, 0))

            elif estado == JUGANDO:
                self.pantalla.blit(self.fondo_nivel, (0, 0))

                # Movimiento jugador
                self.jugador.movimiento_jugador()
                self.jugador.draw(self.pantalla, color=(250, 0, 0))

                # NPC sigue al jugador
                self.npc.seguir(self.jugador)
                self.npc.draw(self.pantalla, color=(0, 0, 250))

            pygame.display.update()
            self.tasa_f.tick(60)

        pygame.quit()


if __name__ == "__main__":
    juego = Juego()
    juego.ejecucion_juego()
    '''
