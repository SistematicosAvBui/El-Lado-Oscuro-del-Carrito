# pruebas_main.py - VERSIÓN CORREGIDA COMPLETA
"""
Pruebas / main consolidado - Pre-Alpha v0.1 -> con crisis e inflación
- 4 NPCs: Comerciante (vendedor), Juan (consumista), Pedro (inversor), Juana (civil)
- Crisis económica: si compras mucho, ingreso pasivo baja y NPCs te culpan
- Inflación: cada compra incrementa el precio del ítem en 2%
- FIXES: Inventario seguro, UI responsive, validaciones completas
"""
import pygame, sys, os, random, time
import math
import personaje2 as per
import colisiones
import dialogos as dialogos_mod
from inventario import Inventario
from ui import UI
from tienda import Tienda, Item
from notificaciones import SistemaNotificaciones
import traceback

pygame.init()
VALUES = (1200, 600)
screen = pygame.display.set_mode(VALUES)
pygame.display.set_caption("El Lado Oscuro del Carrito - PreAlpha v0.1")
clock = pygame.time.Clock()

ASSETS = "assets"

# ====================================================================
# [1] FUNCIÓN DE RUTA DE PYINSTALLER
# ====================================================================

def _obtener_ruta_absoluta(ruta_relativa):
    """Función interna para obtener la ruta absoluta, compatible con PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return ruta_relativa

# ====================================================================
# [2] FUNCIONES DE CARGA MODIFICADAS
# ====================================================================

def cargar_imagen(path, size=None, fallback_color=(80,80,80)):
    ruta_a_cargar = _obtener_ruta_absoluta(path)
    try:
        img = pygame.image.load(ruta_a_cargar).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except Exception:
        s = pygame.Surface(size if size else (100,100))
        s.fill(fallback_color)
        return s

def cargar_animaciones():
    animaciones = []
    for i in range(7):
        ruta_relativa = os.path.join(ASSETS, f"{i}-Photoroom.png")
        ruta_completa = _obtener_ruta_absoluta(ruta_relativa)
        try:
            img = pygame.image.load(ruta_completa).convert_alpha()
            img = pygame.transform.scale(img, (110,130))
        except Exception:
            img = pygame.Surface((110,130), pygame.SRCALPHA)
            img.fill((180,180,180,255))
        animaciones.append(img)
    return animaciones

# ====================================================================
# [3] INICIALIZACIÓN DEL JUEGO
# ====================================================================

try:
    animaciones = cargar_animaciones()

    # ---------- INVENTARIO, UI, TIENDA ----------
    inventario = Inventario(capacidad=10)
    ui = UI(pos_x=50, pos_y=50)
    notificaciones = SistemaNotificaciones()  # NUEVO: Sistema de notificaciones

    # Items (incluyen objetos que aumentan consumo)
    items_tienda = [
        Item("Manzana", "Recupera alimentación", price=50, effect={"alimentacion": +15}),
        Item("Galleta", "Sube recreación", price=80, effect={"recreacion": +20}),
        Item("Libro", "Aumenta recreación", price=200, effect={"recreacion": +40}),
        Item("Celular", "Objeto innecesario: aumenta consumo", price=500, effect={"consumo": +25, "impacto_negativo": True}),
        Item("Tablet", "Objeto innecesario: aumenta consumo fuertemente", price=800, effect={"consumo": +40, "impacto_negativo": True}),
    ]
    tienda = Tienda(items_tienda)

    # ---------- JUGADOR ----------
    dinero_inicial = 1500
    try:
        jugador = per.Protagonista(0, dinero_inicial, animaciones, 250, 350, 5, inventario)
    except Exception:
        jugador = per.Protagonista(0, dinero_inicial, animaciones, 250, 350, 5)
    if not hasattr(jugador, "base_vel"):
        jugador.base_vel = getattr(jugador, "velocidad", 5)

    # ---------- FONDOS Y MAPA ----------
    fondo_menu = cargar_imagen(os.path.join(ASSETS, "imagen_fondo_principal.jpg"), VALUES)
    fondo_nivel = cargar_imagen(os.path.join(ASSETS, "pueblo_del_roble.png"), (1900,1600))
    mapa_rect = fondo_nivel.get_rect()

    # ---------- HITBOXES Y COLISIONES ----------
    hitboxes = [
        pygame.Rect(530, 230, 250, 240),
        pygame.Rect(1115, 230, 245, 250),
        pygame.Rect(530, 680, 230, 220),
        pygame.Rect(1115, 650, 290, 240),
    ]
    sistema_col = colisiones.SistemaColisiones(hitboxes)

    # ---------- ESTADOS ----------
    MENU = "menu"
    JUGANDO = "jugando"
    estado_actual = MENU

    # ---------- FUENTES ----------
    fuente_dialogo = pygame.font.Font(None, 32)
    fuente_interaccion = pygame.font.Font(None, 40)
    fuente_hud = pygame.font.Font(None, 26)
    fuente_big = pygame.font.Font(None, 48)

    # ---------- NPCs ----------
    imagen_vendedor = cargar_imagen(os.path.join(ASSETS, "imagen_vendedor.png"), None)
    try:
        sprite_vendedor = pygame.transform.scale(imagen_vendedor, (100,120))
    except Exception:
        sprite_vendedor = imagen_vendedor

    class NPCSimple:
        def __init__(self, x, y, sprite, name="NPC", role="npc"):
            self.rect = pygame.Rect(x, y, sprite.get_width(), sprite.get_height())
            self.sprite = sprite
            self.name = name
            self.role = role
        def dibujar(self, surf, cam):
            surf.blit(self.sprite, (self.rect.x - cam.x, self.rect.y - cam.y))
        def responder(self, jugador_obj, economic_score):
            if economic_score >= 20:
                if self.role == "consumista":
                    return f"{self.name}: ¡Esto es culpa de compradores excesivos! Mira lo que hiciste."
                if self.role == "inversor":
                    return f"{self.name}: Las ganancias caen por el exceso de consumo; mala gestión."
                if self.role == "vendedor":
                    return f"{self.name}: Las ventas suben... pero la economía sufre. ¿No lo ves?"
                if self.role == "civil":
                    return f"{self.name}: Todos sufrimos ahora. ¿De verdad valía la pena?"
            if jugador_obj.has_item("Celular") or jugador_obj.has_item("Tablet"):
                return f"{self.name}: Vaya, veo que te consientes... eso sube el consumo."
            if self.role == "inversor":
                return f"{self.name}: Si sigue así, la inflación subirá y tus ingresos bajarán."
            if self.role == "consumista":
                return f"{self.name}: ¡Compra! Si no compras te quedas atrás."
            return f"{self.name}: Hola."

    npc_juan_sprite = cargar_imagen(os.path.join(ASSETS, "cuphead.png"), size=(100, 100))
    npc_pedro_sprite = cargar_imagen(os.path.join(ASSETS, "pedro.png"), size=(100, 100))
    npc_juana_sprite = cargar_imagen(os.path.join(ASSETS, "betty.png"), size=(100, 100))

    comerciante = NPCSimple(600, 820, sprite_vendedor, name="Comerciante", role="vendedor")
    juan = NPCSimple(530, 460, npc_juan_sprite, name="Juan", role="consumista")
    pedro = NPCSimple(200, 600, npc_pedro_sprite, name="Pedro", role="inversor")
    juana = NPCSimple(450, 720, npc_juana_sprite, name="Juana", role="civil")

    npc_list = [juan, pedro, juana]

    # ---------- DIALOGO ----------
    dialogo_activo = None
    dialogo_en_progreso = False

    # ---------- CAMARA ----------
    camara = pygame.Vector2(0,0)

    # ---------- HUD / NECESIDADES / CONSUMO / TIMERS / ECONOMIA ----------
    dinero = dinero_inicial
    alimentacion = 100.0
    recreacion = 100.0
    consumo = 0.0

    tiempo_acum_necesidades = 0
    tiempo_acum_ingreso = 0
    INGRESO_INTERVAL_MS = 60_000
    INGRESO_CANTIDAD = 10

    # anuncios
    ANUNCIOS_RUTAS = [
        os.path.join(ASSETS, "anuncio1.png"),
        os.path.join(ASSETS, "anuncio2.png"),
    ]
    ANUNCIOS = [cargar_imagen(p) for p in ANUNCIOS_RUTAS]
    ANUNCIO_INTERVAL_MS = 30_000
    ANUNCIO_DURACION_MS = 5_000
    ultimo_anuncio_ts = pygame.time.get_ticks()
    anuncio_activo = False
    inicio_anuncio_ts = 0
    anuncio_actual = None

    # economía global
    economic_score = 0
    purchases_by_item = {}

    # UI states
    inventario_abierto = False
    tienda_abierta = False
    slot_seleccionado = None
    submenu_abierto = False

    # game over
    game_over = False

    def calcular_ingreso_pasivo(base, economic_score):
        penalty = economic_score * 0.02
        multiplier = max(0.2, 1.0 - penalty)
        return int(base * multiplier)

    def dibujar_hud(surf):
        txt = fuente_hud.render(f"$ {dinero}", True, (255,220,0))
        surf.blit(txt, (VALUES[0] - txt.get_width() - 10, 10))
        ui.barras_estado_simple(surf, "Alimentación", alimentacion, 10, 10)
        ui.barras_estado_simple(surf, "Recreación", recreacion, 10, 40)
        cx = VALUES[0]//2 - 120
        ui.barras_estado_simple(surf, "Consumo", consumo, cx, 10)
        es_txt = fuente_hud.render(f"Impacto económico: {economic_score}", True, (200,200,200))
        surf.blit(es_txt, (VALUES[0] - es_txt.get_width() - 10, 40))

    def dibujar_gameover(surf):
        overlay = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,200))
        surf.blit(overlay, (0,0))
        txt = fuente_big.render("GAME OVER: Consumo Excesivo", True, (255,80,80))
        surf.blit(txt, (VALUES[0]//2 - txt.get_width()//2, VALUES[1]//2 - 80))
        btn_w, btn_h = 160, 48
        bx = VALUES[0]//2 - btn_w - 12
        by = VALUES[1]//2 + 6
        rx = pygame.Rect(bx, by, btn_w, btn_h)
        ry = pygame.Rect(VALUES[0]//2 + 12, by, btn_w, btn_h)
        pygame.draw.rect(surf, (70,200,70), rx, border_radius=8)
        pygame.draw.rect(surf, (200,70,70), ry, border_radius=8)
        f = pygame.font.Font(None, 26)
        surf.blit(f.render("Reintentar", True, (0,0,0)), (rx.x + 30, rx.y + 14))
        surf.blit(f.render("Salir", True, (0,0,0)), (ry.x + 60, ry.y + 14))
        return rx, ry

    # ---------- BUCLE PRINCIPAL ----------
    def main_loop():
        global estado_actual, dialogo_activo, dialogo_en_progreso
        global dinero, alimentacion, recreacion, consumo
        global inventario_abierto, tienda_abierta, slot_seleccionado, submenu_abierto
        global tiempo_acum_necesidades, tiempo_acum_ingreso, ultimo_anuncio_ts
        global anuncio_activo, inicio_anuncio_ts, anuncio_actual, game_over
        global economic_score, purchases_by_item

        while True:
            dt = clock.tick(60)
            ahora = pygame.time.get_ticks()
            tiempo_acum_necesidades += dt
            tiempo_acum_ingreso += dt

            # Generar anuncio
            if not anuncio_activo and ahora - ultimo_anuncio_ts >= ANUNCIO_INTERVAL_MS:
                anuncio_actual = random.choice(ANUNCIOS) if ANUNCIOS else None
                anuncio_activo = True
                inicio_anuncio_ts = ahora
                ultimo_anuncio_ts = ahora

            # Procesar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Game over: solo botones
                if game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        rx, ry = dibujar_gameover(screen)
                        mx, my = event.pos
                        if rx.collidepoint(mx,my):
                            consumo = 0.0
                            game_over = False
                            jugador.eje_x = 250; jugador.eje_y = 350
                            jugador.rect.x = 250; jugador.rect.y = 350
                        if ry.collidepoint(mx,my):
                            pygame.quit(); sys.exit()
                    continue

                # Inventario abierto
                if inventario_abierto:
                    handled = ui.handle_event_inventory(event, inventario)
                    if isinstance(handled, tuple):
                        close, slot_idx, submenu = handled
                        if close:
                            inventario_abierto = False
                            slot_seleccionado = None
                            submenu_abierto = False
                        if slot_idx is not None:
                            slot_seleccionado = slot_idx
                            submenu_abierto = submenu
                    continue

                # Tienda abierta
                if tienda_abierta:
                    handled = tienda.handle_event(event, dinero, jugador, inventario)
                    if isinstance(handled, tuple):
                        close = handled[0]
                        dinero_delta = handled[1] if len(handled)>1 else 0
                        consumo_delta = handled[2] if len(handled)>2 else 0
                        item_name = handled[3] if len(handled)>3 else None
                        if close:
                            tienda_abierta = False
                        if dinero_delta:
                            dinero += dinero_delta
                        if consumo_delta:
                            consumo = min(100.0, consumo + consumo_delta)
                        if item_name:
                            purchases_by_item[item_name] = purchases_by_item.get(item_name, 0) + 1
                            economic_score += 1
                    continue

                # Teclas
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        sistema_col.toggle_debug()
                    if event.key == pygame.K_RETURN and estado_actual == MENU:
                        estado_actual = JUGANDO
                    elif event.key == pygame.K_ESCAPE and estado_actual == JUGANDO:
                        estado_actual = MENU

                    if event.key == pygame.K_m:
                        inventario_abierto = not inventario_abierto
                        slot_seleccionado = None
                        submenu_abierto = False

                    if event.key == pygame.K_e and estado_actual == JUGANDO:
                        # Vendedor
                        if jugador.rect.colliderect(comerciante.rect):
                            tienda_abierta = True
                        else:
                            # NPCs
                            for npc in npc_list:
                                if jugador.rect.colliderect(npc.rect):
                                    resp = npc.responder(jugador, economic_score)
                                    try:
                                        dialogo = dialogos_mod.Dialogo([resp], fuente_dialogo, 100, 450, 1000, 120)
                                        dialogo_activo = dialogo
                                        dialogo_en_progreso = True
                                    except Exception:
                                        dialogo_activo = None
                                        dialogo_en_progreso = False
                                    break

                    if event.key == pygame.K_SPACE and dialogo_en_progreso and dialogo_activo:
                        dialogo_activo.siguiente_linea()

                # ============================================================
                # FIX CRÍTICO: MANEJO SEGURO DE SUBMENU
                # ============================================================
                if submenu_abierto and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    accion = ui.check_submenu_click(mx, my)
                    
                    print(f"[Main] Click en submenu: {accion} en ({mx}, {my})")
                    
                    if accion == "close":
                        # Click fuera del submenu
                        print("[Main] Cerrando submenu (click fuera)")
                        submenu_abierto = False
                        slot_seleccionado = None
                        continue
                    
                    if accion == "usar" and slot_seleccionado is not None:
                        # Validar índice
                        if 0 <= slot_seleccionado < len(inventario.contenido):
                            item = inventario.obtener_item(slot_seleccionado)
                            
                            if item:
                                efectos = getattr(item, "effect", {})
                                alimentacion = min(100.0, alimentacion + efectos.get("alimentacion", 0))
                                recreacion = min(100.0, recreacion + efectos.get("recreacion", 0))
                                consumo = min(100.0, consumo + efectos.get("consumo", 0))
                                
                                # USAR el objeto (lo elimina)
                                item_usado = inventario.usar_objeto(slot_seleccionado)
                                
                                if item_usado:
                                    print(f"[Main] ✓ Item usado: {item.name}")
                                    print(f"[Main] ✓ Alimentación: {alimentacion}, Recreación: {recreacion}")
                                    print(f"[Main] ✓ Items restantes: {len(inventario.contenido)}")
                                    
                                    # NUEVO: Notificación visual
                                    notificaciones.agregar(f"Usaste: {item.name}", "success", 2000)
                                
                                # FIX: Cerrar submenu y deseleccionar
                                submenu_abierto = False
                                slot_seleccionado = None
                                
                                # FIX: NO cerrar inventario para que veas el cambio inmediato
                                # inventario_abierto = False  # <- comentado para ver cambio
                            else:
                                print("[Main] ✗ Error: Item no encontrado")
                                submenu_abierto = False
                                slot_seleccionado = None
                        else:
                            print(f"[Main] ✗ Error: Slot inválido {slot_seleccionado}")
                            submenu_abierto = False
                            slot_seleccionado = None
                    
                    elif accion == "vender" and slot_seleccionado is not None:
                        # Validar índice
                        if 0 <= slot_seleccionado < len(inventario.contenido):
                            item = inventario.obtener_item(slot_seleccionado)
                            
                            if item:
                                precio = getattr(item, "price", 0)
                                
                                # VENDER el objeto (lo elimina)
                                item_vendido = inventario.vender_objeto(slot_seleccionado)
                                
                                if item_vendido:
                                    dinero += precio
                                    print(f"[Main] ✓ Item vendido: {item_vendido.name} por ${precio}")
                                    print(f"[Main] ✓ Dinero actual: ${dinero}")
                                    print(f"[Main] ✓ Items restantes: {len(inventario.contenido)}")
                                    
                                    # NUEVO: Notificación visual
                                    notificaciones.agregar(f"Vendiste: {item_vendido.name} (+${precio})", "success", 2000)
                                
                                # FIX: Cerrar submenu y deseleccionar
                                submenu_abierto = False
                                slot_seleccionado = None
                                
                                # FIX: NO cerrar inventario para que veas el cambio inmediato
                                # inventario_abierto = False  # <- comentado para ver cambio
                            else:
                                print("[Main] ✗ Error: Item no encontrado")
                                submenu_abierto = False
                                slot_seleccionado = None
                        else:
                            print(f"[Main] ✗ Error: Slot inválido {slot_seleccionado}")
                            submenu_abierto = False
                            slot_seleccionado = None
                    
                    elif accion is None:
                        # Click dentro del submenu pero no en botones
                        pass

            # ---------- LOGICA ----------
            if estado_actual == JUGANDO and not game_over:
                # Actualizar notificaciones
                notificaciones.actualizar()
                
                # Velocidad penalizada
                n_items = len(inventario.contenido)
                factor = max(0.3, 1.0 - 0.05 * n_items)
                jugador.velocidad = jugador.base_vel * factor

                # Movimiento
                rect_prev = jugador.rect.copy()
                try:
                    jugador.movimiento(hitboxes)
                except TypeError:
                    try:
                        jugador.movimiento()
                    except Exception:
                        pass

                dx = jugador.rect.x - rect_prev.x
                dy = jugador.rect.y - rect_prev.y
                jugador.rect = sistema_col.prevenir_movimiento(rect_prev, dx, dy)
                jugador.eje_x = jugador.rect.x
                jugador.eje_y = jugador.rect.y
                jugador.rect.clamp_ip(mapa_rect)

                # Necesidades
                if tiempo_acum_necesidades >= 8000:
                    alimentacion = max(0.0, alimentacion - 1.0)
                    recreacion = max(0.0, recreacion - 1.0)
                    tiempo_acum_necesidades = 0

                # Ingreso pasivo
                if tiempo_acum_ingreso >= INGRESO_INTERVAL_MS:
                    ingreso_real = calcular_ingreso_pasivo(INGRESO_CANTIDAD, economic_score)
                    dinero += ingreso_real
                    tiempo_acum_ingreso = 0

                # Game over
                if consumo >= 90.0:
                    game_over = True

            # ---------- RENDER ----------
            if estado_actual == JUGANDO:
                objetivo_x = jugador.rect.centerx - VALUES[0] // 2
                objetivo_y = jugador.rect.centery - VALUES[1] // 2
                objetivo_x = max(0, min(objetivo_x, mapa_rect.width - VALUES[0]))
                objetivo_y = max(0, min(objetivo_y, mapa_rect.height - VALUES[1]))
                lerp_factor = 0.15
                camara.x += (objetivo_x - camara.x) * lerp_factor
                camara.y += (objetivo_y - camara.y) * lerp_factor

            if estado_actual == MENU:
                screen.blit(fondo_menu, (0,0))

            elif estado_actual == JUGANDO:
                screen.blit(fondo_nivel, (-camara.x, -camara.y))

                try:
                    comerciante.dibujar(screen, camara)
                except Exception:
                    pass
                for npc in npc_list:
                    npc.dibujar(screen, camara)

                try:
                    jugador.dibujar(screen, camara)
                except Exception:
                    pygame.draw.rect(screen, (0,120,255),
                                     (jugador.rect.x - camara.x, jugador.rect.y - camara.y,
                                      jugador.rect.width, jugador.rect.height))

                sistema_col.dibujar_debug(screen, camara)

                # Indicador E
                mostrar_e = False
                if jugador.rect.colliderect(comerciante.rect.inflate(20,20)):
                    mostrar_e = True
                else:
                    for npc in npc_list:
                        if jugador.rect.colliderect(npc.rect.inflate(20,20)):
                            mostrar_e = True
                            break

                if mostrar_e:
                    te = fuente_interaccion.render("E", True, (255,255,255))
                    screen.blit(te, (jugador.rect.centerx - camara.x - 8,
                                     jugador.rect.top - 30 - camara.y))

                dibujar_hud(screen)

            # Interfaces
            if inventario_abierto:
                ui.draw_inventory(screen, inventario,
                                     slot_selected=slot_seleccionado,
                                     open_submenu=submenu_abierto)
            if tienda_abierta:
                tienda.draw(screen)
            if submenu_abierto and slot_seleccionado is not None:
                ui.draw_submenu(screen)

            # Diálogo
            if dialogo_en_progreso and dialogo_activo:
                dialogo_activo.actualizar(dt)
                dialogo_activo.dibujar(screen)
                if not dialogo_activo.en_dialogo:
                    dialogo_en_progreso = False
            
            # NUEVO: Notificaciones (encima de diálogos)
            notificaciones.dibujar(screen)

            # Anuncio
            if anuncio_activo and anuncio_actual:
                ax = VALUES[0]//2 - anuncio_actual.get_width()//2
                ay = VALUES[1]//2 - anuncio_actual.get_height()//2
                screen.blit(anuncio_actual, (ax, ay))
                if ahora - inicio_anuncio_ts >= ANUNCIO_DURACION_MS:
                    anuncio_activo = False
                    anuncio_actual = None

            # Game over
            if game_over:
                dibujar_gameover(screen)

            pygame.display.update()

    if __name__ == "__main__":
        main_loop()

except Exception as e:
    print("\n\n#####################################################")
    print("## ERROR CRÍTICO: FALLO AL INICIAR LA APLICACIÓN ##")
    print("#####################################################")
    print(f"Error específico: {e}\n")
    traceback.print_exc()
    print("\n--- PASO CLAVE ---")
    print("El error anterior indica que un archivo no se encontró.")
    print("Asegúrate de compilar con: pyinstaller --onefile --console --add-data 'assets;assets' src/python/pruebas_main.py")
    print("------------------")
    input("Presiona ENTER para cerrar la ventana y salir...")
    sys.exit(1)