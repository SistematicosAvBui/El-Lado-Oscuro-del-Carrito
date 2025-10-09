import pygame
import sys
import personaje2 as per
import textos
import time

pygame.init()
values = (1200, 600)
screen = pygame.display.set_mode(values)
pygame.display.set_caption("El Lado Oscuro del Carrito")
clock = pygame.time.Clock()

aparicion_x, aparicion_y = 250, 350
dinero = 1500

# --- CARGAR ANIMACIONES ---
def cargar_animaciones():
    animaciones = []
    for frame in range(7):
        img = pygame.image.load(f"assets/{frame}-Photoroom.png").convert_alpha()
        img = pygame.transform.scale(img, (110, 130))
        animaciones.append(img)
    return animaciones

animaciones = cargar_animaciones()
jugador = per.Protagonista(0, dinero, animaciones, aparicion_x, aparicion_y, 5)

# --- FONDOS ---
fondo_menu = pygame.image.load("assets/imagen_fondo_principal.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, values)

fondo_nivel = pygame.image.load("assets/fondo_ciudad_del_consumo.png")
fondo_nivel = pygame.transform.scale(fondo_nivel, (1900, 1600))
mapa_rect = fondo_nivel.get_rect()

# --- ESTADOS DEL JUEGO ---
MENU = "menu"
JUGANDO = "jugando"
estado_actual = MENU

# --- FUENTE PARA DIÁLOGO Y TECLA E ---
fuente_dialogo = pygame.font.Font(None, 32)
fuente_interaccion = pygame.font.Font(None, 40)

# --- CREACIÓN DEL NPC ---
dialogos_vendedor = [
    "¡Hola, joven consumidor!",
    "Parece que tienes dinero fresco...",
    "Aquí todo está en oferta... aunque no por mucho tiempo.",
    "Recuerda: ¡comprar es invertir en la felicidad del sistema!"
]
imagen_vendedor = pygame.image.load("assets/imagen_vendedor.png").convert_alpha()
sprite_vendedor = pygame.transform.scale(imagen_vendedor, (100, 120))
vendedor = per.NPC(0, 9999, 600, 350, dialogos_vendedor, sprite_vendedor)

# --- ESTADO DEL DIÁLOGO ---
dialogo_activo = None
dialogo_en_progreso = False

# --- CÁMARA ---
camara = pygame.Vector2(0, 0)

# --- LOOP PRINCIPAL ---
while True:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # --- CAMBIO DE ESTADO ---
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if estado_actual == MENU:
                estado_actual = JUGANDO
        if event.type == pygame.K_ESCAPE:
                if estado_actual == JUGANDO:
                    estado_actual = MENU

        # --- INTERACCIÓN CON NPC ---
        if estado_actual == JUGANDO and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and jugador.rect.colliderect(vendedor.rect):
                if not dialogo_en_progreso:
                    dialogo_activo = textos.Dialogo(
                        vendedor.dialogos, fuente_dialogo, 100, 450, 1000, 120
                    )
                    dialogo_en_progreso = True

            elif event.key == pygame.K_SPACE and dialogo_en_progreso and dialogo_activo:
                dialogo_activo.siguiente_linea()

    # --- DIBUJO Y LÓGICA ---
    if estado_actual == MENU:
        screen.blit(fondo_menu, (0, 0))

    elif estado_actual == JUGANDO:
        # --- Movimiento del jugador (usa su propio método) ---
        jugador.movimiento()

        # --- Limitar jugador al mapa ---
        jugador.rect.clamp_ip(mapa_rect)

        # --- Actualizar cámara ---
        camara.x = jugador.rect.centerx - values[0] // 2
        camara.y = jugador.rect.centery - values[1] // 2

        # --- Limitar cámara al mapa ---
        camara.x = max(0, min(camara.x, mapa_rect.width - values[0]))
        camara.y = max(0, min(camara.y, mapa_rect.height - values[1]))

        # --- DIBUJAR ESCENA ---
        screen.blit(fondo_nivel, (-camara.x, -camara.y))

        # Dibujar NPC y jugador con coordenadas relativas a cámara
        screen.blit(vendedor.sprite, (vendedor.rect.x - camara.x, vendedor.rect.y - camara.y))
        jugador.dibujar(screen, camara)

        # --- MOSTRAR "E" SOLO SI ESTÁ CERCA ---
        if jugador.rect.colliderect(vendedor.rect.inflate(20, 20)):
            texto_e = fuente_interaccion.render("E", True, (255, 255, 255))
            e_x = vendedor.rect.centerx - texto_e.get_width() // 2 - camara.x
            e_y = vendedor.rect.top - 35 - camara.y
            screen.blit(texto_e, (e_x, e_y))

        # --- DIÁLOGO ---
        if dialogo_en_progreso and dialogo_activo:
            dialogo_activo.actualizar(dt)
            dialogo_activo.dibujar(screen)
            if not dialogo_activo.en_dialogo:
                dialogo_en_progreso = False

    pygame.display.update()



