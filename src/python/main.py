import pygame 
import personaje as per

class Juego():
    def ejecucion_juego(self):
        pygame.init()
        pantalla = pygame.display.set_mode((1200, 600))
        tasa_f = pygame.time.Clock()

        MENU = "menu"
        JUGANDO = "jugando"
        estado = MENU  

        fondo_menu = pygame.image.load("assets/imagen_fondo_principal2.png")

        fondo_menu = pygame.transform.scale(fondo_menu, (1200, 600)) 

        jugador = per.Jugador(100, 100, 3, 30, 50)

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
                pantalla.blit(fondo_menu, (0, 0)) 

            elif estado == JUGANDO:
                pantalla.fill((0, 0, 0))  

                jugador.movimiento_jugador()
                pygame.draw.rect(
                    pantalla, 
                    (250, 0, 0),
                    (jugador.eje_x, jugador.eje_y, jugador.ancho, jugador.alto)
                )

            pygame.display.update()
            tasa_f.tick(30)
            pygame.display.set_caption("El Lado Oscuro del Carrito")

        pygame.quit()

el_lado_oscuro = Juego()
el_lado_oscuro.ejecucion_juego()


