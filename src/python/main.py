import pygame
import sys
import personajes as per

pygame.init()
values = (1200, 600)
screen = pygame.display.set_mode(values)
pygame.display.set_caption("El Lado Oscuro del Carrito")
clock = pygame.time.Clock()
def cargar_animaciones():
    """Carga todas las animaciones del personaje"""
    animaciones = []
    try:
        # Intentar cargar frames 0-6 (7 frames total)
        for frame in range(7):
            img = pygame.image.load(f"assets/{frame}-Photoroom.png")
            img = pygame.transform.scale(img, (150, 175))
            animaciones.append(img)
    except pygame.error:
        # Si no se pueden cargar las animaciones, usar una imagen por defecto
        print("No se pudieron cargar las animaciones, usando imagen por defecto")
        img = pygame.image.load("assets/2-Photoroom.png")
        img = pygame.transform.scale(img, (150, 175))
        animaciones = [img] * 7  # Repetir la misma imagen
    
    return animaciones

animaciones = cargar_animaciones()
jugador = per.Protagonista(0, 1500, animaciones, 250, 350, 5)

# Fondos
fondo_menu = pygame.image.load("assets/imagen_fondo_principal.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, (1200, 600))

fondo_nivel = pygame.image.load("assets/imagen_nivel.jpg")
fondo_nivel = pygame.transform.scale(fondo_nivel, (1200, 600))

# Estados del juego
MENU = "menu"
JUGANDO = "jugando"
estado_actual = MENU

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event.type)
            sys.exit()
        
        # Cambiar estado con Enter
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if estado_actual == MENU:
                estado_actual = JUGANDO
            elif estado_actual == JUGANDO:
                estado_actual = MENU

    # Dibujar según el estado actual
    if estado_actual == MENU:
        screen.blit(fondo_menu, (0, 0))
        # No dibujar el personaje en el menú
    elif estado_actual == JUGANDO:
        screen.blit(fondo_nivel, (0, 0))
        # Solo mover y dibujar el personaje cuando se está jugando
        jugador.movimiento()
        jugador.dibujar(screen)
    
    pygame.display.update()
    clock.tick(60)

