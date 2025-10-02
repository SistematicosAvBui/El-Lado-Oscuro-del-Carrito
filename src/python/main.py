import pygame
import sys
import personajes as per

pygame.init()
values = (1200, 600)
screen = pygame.display.set_mode(values)
pygame.display.set_caption("El Lado Oscuro del Carrito")
clock = pygame.time.Clock()
def actualizar_animacion (comienzo_iteracion, indice_animacion):
    animaciones = []
    for frame in range(comienzo_iteracion, indice_animacion):
        img = pygame.image.load(f"assets/{frame}-Photoroom.png")
        img = pygame.transform.scale(img, (150, 175))
        animaciones.append(img)
    return animaciones
imagen = actualizar_animacion(0, 7)
jugador = per.Protagonista(0, 1500, imagen, 100, 300, 5)
fondo_menu = pygame.image.load("assets/imagen_fondo_principal.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, (1200, 600))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event.type)
            sys.exit()

    screen.blit(fondo_menu, (0, 0))
    jugador.movimiento()
    jugador.dibujar(screen)
    
    

    pygame.display.update()
    clock.tick(60)

        

