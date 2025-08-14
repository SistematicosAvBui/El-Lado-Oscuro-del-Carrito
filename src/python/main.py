import pygame 
import personaje as per

class Juego():
    def ejecucion_juego(self):
        pygame.init()
        pantalla = pygame.display.set_mode((1200, 600))
        jugador = per.Jugador(0, 0, 3, 30, 50)
        tasa_f = pygame.time.Clock()
        estado = True
        
        while estado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    estado = False
            
            jugador.movimiento_jugador()
            
            pantalla.fill((0, 0, 0))
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

