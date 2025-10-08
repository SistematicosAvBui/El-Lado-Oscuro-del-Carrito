import pygame

class Dialogo:
    def __init__(self, texto, fuente, x, y, ancho, alto):
        self.textos = texto if isinstance(texto, list) else [texto]
        self.indice_texto = 0
        self.fuente = fuente
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_caja = (30, 30, 30)
        self.color_texto = (255, 255, 255)
        self.velocidad = 30 
        self.texto_actual = ""
        self.tiempo = 0
        self.en_dialogo = True

    def actualizar(self, dt):
        if not self.en_dialogo:
            return

        texto_completo = self.textos[self.indice_texto]
        if len(self.texto_actual) < len(texto_completo):
            self.tiempo += dt
            if self.tiempo > 1000 / self.velocidad:
                self.texto_actual += texto_completo[len(self.texto_actual)]
                self.tiempo = 0

    def siguiente_linea(self):
        if self.indice_texto < len(self.textos) - 1:
            self.indice_texto += 1
            self.texto_actual = ""
        else:
            self.en_dialogo = False

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color_caja, self.rect, border_radius=15)
        texto_surface = self.fuente.render(self.texto_actual, True, self.color_texto)
        pantalla.blit(texto_surface, (self.rect.x + 20, self.rect.y + 20))
