import pygame
import sys
import personaje2 as per
import colisiones
import textos
import cambio_escenarios as tel

# --- CONFIGURACIÓN BÁSICA ---
pygame.init()
values = (1200, 600)
screen = pygame.display.set_mode(values)
pygame.display.set_caption("El Lado Oscuro del Carrito")
clock = pygame.time.Clock()

# --- POSICIÓN INICIAL DEL JUGADOR ---
aparicion_x, aparicion_y = 250, 350
dinero = 1500

# --- CARGAR ANIMACIONES DEL JUGADOR ---
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

fondo_nivel = pygame.image.load("assets/pueblo_del_roble.png")
fondo_nivel = pygame.transform.scale(fondo_nivel, (1900, 1600))
mapa_rect = fondo_nivel.get_rect()

# --- HITBOXES DEL MUNDO ---
hitboxes = [
    pygame.Rect(530, 230, 250, 240),   # Edificio superior izquierdo
    pygame.Rect(1115, 230, 245, 250),  # Edificio superior derecho
    pygame.Rect(530, 680, 230, 220),   # Edificio de la Tienda
    pygame.Rect(1115, 650, 290, 240),  # Edificio del Banco
]

# -- Zona Teleport

teleports = [
    tel.ZonaTeleport(605, 470, 80, 20, None),
    tel.ZonaTeleport(1200, 470, 70, 20, None),
    tel.ZonaTeleport(605, 900, 80, 20, None),
    tel.ZonaTeleport(1200, 890, 110, 20, None),
]

# --- Sistema de colisiones ---
sistema_col = colisiones.SistemaColisiones(hitboxes)

# --- ESTADOS DEL JUEGO ---
MENU = "menu"
JUGANDO = "jugando"
estado_actual = MENU

# --- FUENTES ---
fuente_dialogo = pygame.font.Font(None, 32)
fuente_interaccion = pygame.font.Font(None, 40)

# --- NPC ---
dialogos_vendedor = [
    "¡Hola, joven consumidor!",
    "Parece que tienes dinero fresco...",
    "Aquí todo está en oferta... aunque no por mucho tiempo.",
    "Recuerda: ¡comprar es invertir en la felicidad del sistema!"
]
imagen_vendedor = pygame.image.load("assets/imagen_vendedor.png").convert_alpha()
sprite_vendedor = pygame.transform.scale(imagen_vendedor, (100, 120))
vendedor = per.NPC(0, 9999, 600, 820, dialogos_vendedor, sprite_vendedor)

# --- DIÁLOGO ---
dialogo_activo = None
dialogo_en_progreso = False

# --- CÁMARA ---
camara = pygame.Vector2(0, 0)

# --- SISTEMA DE TELETRANSPORTE ---

scenary_switch = tel.Teletransporte (teleports)


# --- LOOP PRINCIPAL ---
while True:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # toggle debug con D
            if event.key == pygame.K_0:
                sistema_col.toggle_debug()

            if event.key == pygame.K_RETURN and estado_actual == MENU:
                estado_actual = JUGANDO
            elif event.key == pygame.K_ESCAPE and estado_actual == JUGANDO:
                estado_actual = MENU

            # --- INTERACCIÓN CON NPC ---
            if estado_actual == JUGANDO:
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
        # Guardamos la posición previa del rect (coordenadas del mundo)
        rect_prev = jugador.rect.copy()

        # --- Movimiento del jugador (tu método existente) ---
        # (tu Protagonista.movimiento() actualiza eje_x/eje_y y jugador.rect)
        jugador.movimiento()

        # Calculamos el delta (dx, dy) en mundo (después de que movimiento() actualizó rect)
        dx = jugador.rect.x - rect_prev.x
        dy = jugador.rect.y - rect_prev.y

        # DEBUG prints (quita cuando esté OK)
        # print("prev:", rect_prev.topleft, "dx,dy:", dx, dy)

        # Usamos el sistema de colisiones para prevenir movimiento
        rect_corregido = sistema_col.prevenir_movimiento(rect_prev, dx, dy)

        # Aplicamos la rect_corregido al jugador (sin tocar eje_x/eje_y internos)
        jugador.rect = rect_corregido
        jugador.eje_x = jugador.rect.x
        jugador.eje_y = jugador.rect.y

        # --- Limitar jugador al mapa ---
        jugador.rect.clamp_ip(mapa_rect)
        jugador.eje_x = jugador.rect.x
        jugador.eje_y = jugador.rect.y

        # --- Actualizar cámara ---
        camara.x = jugador.rect.centerx - values[0] // 2
        camara.y = jugador.rect.centery - values[1] // 2
        camara.x = max(0, min(camara.x, mapa_rect.width - values[0]))
        camara.y = max(0, min(camara.y, mapa_rect.height - values[1]))

        # --- DIBUJAR ESCENA ---
        screen.blit(fondo_nivel, (-camara.x, -camara.y))

        # Dibujar NPC y jugador con cámara
        screen.blit(vendedor.sprite, (vendedor.rect.x - camara.x, vendedor.rect.y - camara.y))
        # Se asume que Protagonista.dibujar acepta (surface, camara)
        try:
            jugador.dibujar(screen, camara)
        except TypeError:
            # Fallback: método dibujar sin camara (antiguo)
            # dibuja usando jugador.rect que ya está en coordenadas mundo
            current_frame = jugador.get_current_frame()
            screen.blit(current_frame, (jugador.rect.x - camara.x, jugador.rect.y - camara.y))

        # --- DIBUJAR HITBOXES (debug) ---
        sistema_col.dibujar_debug(screen, camara)

        # dibujar teleports y hitboxes visibles (para debug)
        if sistema_col.debug_mode:
            for rect in hitboxes:
                r = pygame.Rect(rect.x - camara.x, rect.y - camara.y, rect.width, rect.height)
                pygame.draw.rect(screen, (255, 0, 0), r, 2)
            for rect in teleports:
                r = pygame.Rect(rect.x - camara.x, rect.y - camara.y, rect.width, rect.height)
                pygame.draw.rect(screen, (0, 255, 0), r, 2)

        # Identificamos el teleport 
        delta_time = clock.get_time
        nuevo_fondo = scenary_switch.deteccion(jugador, hitboxes, delta_time)
        if nuevo_fondo:
            fondo_nivel = nuevo_fondo

        # --- MOSTRAR "E" ---
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
