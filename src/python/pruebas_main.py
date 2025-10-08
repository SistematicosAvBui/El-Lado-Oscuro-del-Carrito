import pygame
import sys
import personajes as per
import textos  # <-- 📦 Importamos el módulo de diálogos
import time

pygame.init()
values = (1200, 600)
screen = pygame.display.set_mode(values)
pygame.display.set_caption("El Lado Oscuro del Carrito")
clock = pygame.time.Clock()
aparicion_x, aparicion_y = 250, 350
hitbox_values = [(0, 0, 265, 220), (270, 0, 240, 150), (790, 0, 780, 360), (0, 600 - 215, 220, 225), (220, 600 -70, 800, 35), (1000, 600 - 155, 200, 165)]
dinero = 1500


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
jugador = per.Protagonista(0, dinero, animaciones, aparicion_x, aparicion_y, 5)

# Fondos
fondo_menu = pygame.image.load("assets/imagen_fondo_principal.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, (1200, 600))

fondo_nivel = pygame.image.load("assets/imagen_nivel.jpg")
fondo_nivel = pygame.transform.scale(fondo_nivel, (1200, 600))

# Estados del juego
MENU = "menu"
JUGANDO = "jugando"
estado_actual = MENU

### --------------------------------------------------------
### NUEVO: Fuente base para los textos del diálogo
### --------------------------------------------------------
fuente_dialogo = pygame.font.Font(None, 32)

### --------------------------------------------------------
### NUEVO: Creación del NPC vendedor y su diálogo
### --------------------------------------------------------
dialogos_vendedor = [
    "¡Hola, joven consumidor!",
    "Parece que tienes dinero fresco...",
    "Aquí todo está en oferta... aunque no por mucho tiempo.",
    "Recuerda: ¡comprar es invertir en la felicidad del sistema!"
]
imagen_vendedor = pygame.image.load("assets/imagen_vendedor.png").convert_alpha()
sprite_vendedor = pygame.transform.scale(imagen_vendedor, (115, 160))
vendedor = per.NPC(0, 9999, 600, 300, dialogos_vendedor, sprite_vendedor)

### --------------------------------------------------------
### NUEVO: Caja de diálogo (inicialmente inactiva)
### --------------------------------------------------------
dialogo_activo = None
dialogo_en_progreso = False


while True:
    dt = clock.tick(60)
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

        ### --------------------------------------------------------
        ### NUEVO: Control del diálogo con tecla E y avance con espacio
        ### --------------------------------------------------------
        if estado_actual == JUGANDO and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if jugador.rect.colliderect(vendedor.rect) and not dialogo_en_progreso:
                    # Iniciar diálogo
                    dialogo_activo = textos.Dialogo(
                        vendedor.dialogos,
                        fuente_dialogo,
                        100, 450, 1000, 120
                    )
                    dialogo_en_progreso = True

            elif event.key == pygame.K_SPACE and dialogo_en_progreso and dialogo_activo:
                dialogo_activo.siguiente_linea()


    # Dibujar según el estado actual
    if estado_actual == MENU:
        screen.blit(fondo_menu, (0, 0))

    elif estado_actual == JUGANDO:
        screen.blit(fondo_nivel, (0, 0))
        
        # Convertir hitbox_values a rectángulos de pygame
        obstaculos = [pygame.Rect(x, y, w, h) for x, y, w, h in hitbox_values]
        
        jugador.movimiento(obstaculos)
        jugador.dibujar(screen)

        ### --------------------------------------------------------
        ### NUEVO: Dibujar al vendedor
        ### --------------------------------------------------------
        vendedor.dibujar(screen)  # Rectángulo visible (temporal)

        ### --------------------------------------------------------
        ### NUEVO: Actualizar y dibujar el diálogo si está activo
        ### --------------------------------------------------------
        if dialogo_en_progreso and dialogo_activo:
            dialogo_activo.actualizar(dt)
            dialogo_activo.dibujar(screen)
            if not dialogo_activo.en_dialogo:
                dialogo_en_progreso = False  # Finaliza diálogo

        # Dibujar obstáculos (debug)
        for obstaculo in obstaculos:
            pygame.Rect(obstaculo)

        # Rectángulos para cambiar de mapa
        map_switch_rects = []
        background2 = pygame.Rect(510, 0, 300, 10)
        map_switch_rects.append(background2)
        pygame.Rect(background2)
        up_background1 = pygame.Rect(400, 590, 800, 10)
        map_switch_rects.append(up_background1)
        pygame.Rect(up_background1)
        
        # Verificar colisión con el rectángulo de cambio de mapa
        if jugador.rect.colliderect(map_switch_rects[0]):
            fondo_nivel = pygame.image.load("assets/imagen_fondo2.jpg")
            fondo_nivel = pygame.transform.scale(fondo_nivel, (1200, 600))
            hitbox_values = []
            jugador.eje_x = 600
            jugador.eje_y = 350
            jugador.rect.x = 600
            jugador.rect.y = 350
            
        if jugador.rect.colliderect(map_switch_rects[1]):
            fondo_nivel = pygame.image.load("assets/imagen_nivel.jpg")
            fondo_nivel = pygame.transform.scale(fondo_nivel, (1200, 600))
            hitbox_values = [(0, 0, 265, 220), (270, 0, 240, 150), (790, 0, 780, 360), (0, 600 - 215, 220, 225), (220, 600 -70, 800, 35), (1000, 600 - 155, 200, 165)]
            jugador.eje_y = 50
            jugador.rect.x = 600
            jugador.rect.y = 50

    pygame.display.update()
