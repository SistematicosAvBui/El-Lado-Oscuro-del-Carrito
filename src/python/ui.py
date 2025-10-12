import pygame

class UI():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 32)
        self.color_texto = (255, 255, 255)

    def interfaz_inventario(self, jugador, surface):
        pygame.draw.rect(surface, (30, 30, 30), (50, 50, 500, 500), 0)

    def barras_estados(self, estados: dict, surface, eje_x, eje_y):
        _maximo = 100
        ancho_maximo = 200
        alto_barra = 20
        espacio_vertical = 40

        for indice, (nombre, valor_actual) in enumerate(estados.items()):
            porcentaje = valor_actual / _maximo
            porcentaje = max(0, min(1, porcentaje))
            ancho_actual = int(ancho_maximo * porcentaje)

            pos_y = eje_y + indice * espacio_vertical

            pygame.draw.rect(surface, (0, 0, 0), (eje_x, pos_y, ancho_maximo, alto_barra))

            if porcentaje > 0.6:
                color_relleno = (0, 255, 0)
            elif porcentaje > 0.3:
                color_relleno = (255, 255, 0)
            else:
                color_relleno = (255, 0, 0)

            pygame.draw.rect(surface, color_relleno, (eje_x, pos_y, ancho_actual, alto_barra))

            texto_barras = self.font.render(f"{nombre}: {valor_actual}", True, self.color_texto)
            surface.blit(texto_barras, (eje_x + ancho_maximo + 15, pos_y - 2))
