import pygame

class UI():
    def __init__(self, pos_x, pos_y):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 32)
        self.color_texto = (255, 255, 255)
        self.pos_x = pos_x
        self.pos_y = pos_y


    def interfaz_inventario(self, surface, capacidad):
    # --- Parámetros de interfaz ---
        ancho_interfaz, alto_interfaz = 800, 600
        columnas = 5
        filas = 2
        espaciado = 15  # separación entre slots
    
    # --- Fondo del inventario ---
        pygame.draw.rect(surface, (30, 30, 30), (self.pos_x, self.pos_y, ancho_interfaz, alto_interfaz))
        pygame.draw.rect(surface, (60, 60, 60), (self.pos_x - 4, self.pos_y - 4, ancho_interfaz + 8, alto_interfaz + 8), 4)

    # --- Cálculo del tamaño de cada slot ---
        ancho_slot = (ancho_interfaz - (espaciado * (columnas + 1))) // columnas
        alto_slot = (alto_interfaz - (espaciado * (filas + 1))) // filas

        slots = []

    # --- Dibujar slots en cuadrícula ---
        for fila in range(filas):
            for columna in range(columnas):
                indice = fila * columnas + columna
                if indice >= capacidad:
                    break  # no dibuja más si supera la capacidad

                pos_x = self.pos_x + espaciado + columna * (ancho_slot + espaciado)
                pos_y = self.pos_y + espaciado + fila * (alto_slot + espaciado)

                rect = pygame.Rect(pos_x, pos_y, ancho_slot, alto_slot)
                pygame.draw.rect(surface, (80, 80, 80), rect)        
                pygame.draw.rect(surface, (150, 150, 150), rect, 2)  
                slots.append(rect)

        return slots


    def barras_estados(self, estados: dict, surface, eje_x, eje_y):
        maximo = 100
        ancho_maximo = 200
        alto_barra = 20
        espacio_vertical = 40

        for indice, (nombre, valor_actual) in enumerate(estados.items()):
            porcentaje = valor_actual / maximo
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

