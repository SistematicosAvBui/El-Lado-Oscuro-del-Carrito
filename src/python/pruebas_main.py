# pruebas_main.py - INTEGRACIÓN COMPLETA DE MECÁNICAS ANTI-CONSUMISMO
"""
Versión: Pre-Alpha v0.2 - Mecánicas Anti-Consumismo Integradas

NUEVAS CARACTERÍSTICAS:
✅ Sistema "Necesidad vs Deseo" - Popup reflexivo antes de comprar
✅ Impacto Visual del Mundo - Basura y filtros según contaminación
✅ Comparador de Productos - Tabla ecológica (presiona C en tienda)
✅ Indicador de contaminación en tiempo real
✅ Partículas atmosféricas en niveles críticos
✅ Diálogos NPCs dinámicos según contaminación

CONTROLES:
- WASD/Flechas: Mover
- E: Interactuar con NPCs/Tienda
- M: Abrir inventario
- C: Comparador de productos (en tienda)
- SPACE: Avanzar diálogo
- ESC: Cerrar interfaces
- P: Debug colisiones
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
from mecanicas_anticonsumo import CoordinadorAntiConsumo
from popup_decision import PopupDecision
from comparador_productos import ComparadorProductos
from impacto_visual_mundo import GestorImpactoVisual, ParticulasAtmosfericas

pygame.init()
VALUES = (1200, 600)
screen = pygame.display.set_mode(VALUES)
pygame.display.set_caption("El Lado Oscuro del Carrito - PreAlpha v0.2")
clock = pygame.time.Clock()

ASSETS = "assets"

# ====================================================================
# FUNCIONES DE CARGA
# ====================================================================

def _obtener_ruta_absoluta(ruta_relativa):
    """Compatible con PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return ruta_relativa

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
# INICIALIZACIÓN
# ====================================================================

try:
    animaciones = cargar_animaciones()

    # ---------- INVENTARIO, UI, TIENDA ----------
    inventario = Inventario(capacidad=10)
    ui = UI(pos_x=50, pos_y=50)
    notificaciones = SistemaNotificaciones()

    # Items (incluyen impacto ambiental)
    items_tienda = [
        Item("Manzana", "Recupera alimentación", price=50, effect={"alimentacion": +15}),
        Item("Galleta", "Sube recreación", price=80, effect={"recreacion": +20}),
        Item("Libro", "Aumenta recreación", price=200, effect={"recreacion": +40}),
        Item("Celular", "Objeto innecesario: aumenta consumo", price=500, effect={"consumo": +25, "impacto_negativo": True}),
        Item("Tablet", "Objeto innecesario: aumenta consumo fuertemente", price=800, effect={"consumo": +40, "impacto_negativo": True}),
    ]
    tienda = Tienda(items_tienda)

    # ---------- SISTEMAS ANTI-CONSUMISMO ----------
    coordinador_anticonsumo = CoordinadorAntiConsumo()
    popup_decision = PopupDecision(screen_size=VALUES)
    comparador_productos = ComparadorProductos(
        screen_size=VALUES,
        base_datos_productos=coordinador_anticonsumo.base_datos
    )
    
    # ---------- FONDOS Y MAPA (ANTES DE GESTOR IMPACTO) ----------
    fondo_menu = cargar_imagen(os.path.join(ASSETS, "imagen_fondo_principal.jpg"), VALUES)
    fondo_nivel = cargar_imagen(os.path.join(ASSETS, "pueblo_del_roble.png"), (1900,1600))
    mapa_rect = fondo_nivel.get_rect()  # ✅ AHORA sí existe
    
    # ✅ FIX: Ahora inicializar DESPUÉS de mapa_rect
    gestor_impacto_visual = GestorImpactoVisual(
        screen_size=VALUES,
        mapa_size=(mapa_rect.width, mapa_rect.height)
    )
    particulas_atmosfera = ParticulasAtmosfericas(screen_size=VALUES)
    
    print("[Main] ✓ Sistemas anti-consumismo inicializados correctamente")

    # Estado del popup
    esperando_decision_compra = False
    item_pendiente_compra = None
    precio_pendiente = 0

    # ---------- JUGADOR ----------
    dinero_inicial = 1500
    try:
        jugador = per.Protagonista(0, dinero_inicial, animaciones, 250, 350, 5, inventario)
    except Exception:
        jugador = per.Protagonista(0, dinero_inicial, animaciones, 250, 350, 5)
    if not hasattr(jugador, "base_vel"):
        jugador.base_vel = getattr(jugador, "velocidad", 5)

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
        
        def responder(self, jugador_obj, economic_score, estado_mundo):
            """
            ✅ NUEVO: Respuesta dinámica según contaminación
            """
            # Prioridad 1: Diálogo ambiental si contaminación alta
            dialogo_ambiental = coordinador_anticonsumo.get_dialogo_npc(self.role)
            if dialogo_ambiental:
                return f"{self.name}: {dialogo_ambiental}"
            
            # Prioridad 2: Diálogo por crisis económica
            if economic_score >= 20:
                if self.role == "consumista":
                    return f"{self.name}: ¡Esto es culpa de compradores excesivos! Mira lo que hiciste."
                if self.role == "inversor":
                    return f"{self.name}: Las ganancias caen por el exceso de consumo; mala gestión."
                if self.role == "vendedor":
                    return f"{self.name}: Las ventas suben... pero la economía sufre. ¿No lo ves?"
                if self.role == "civil":
                    return f"{self.name}: Todos sufrimos ahora. ¿De verdad valía la pena?"
            
            # Prioridad 3: Comentario sobre items consumistas
            if jugador_obj.has_item("Celular") or jugador_obj.has_item("Tablet"):
                return f"{self.name}: Vaya, veo que te consientes... eso sube el consumo."
            
            # Diálogo default por rol
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

    # Anuncios
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

    # Economía global
    economic_score = 0
    purchases_by_item = {}

    # UI states
    inventario_abierto = False
    tienda_abierta = False
    slot_seleccionado = None
    submenu_abierto = False

    # Game over
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

    # ====================================================================
    # BUCLE PRINCIPAL
    # ====================================================================

    def main_loop():
        global estado_actual, dialogo_activo, dialogo_en_progreso
        global dinero, alimentacion, recreacion, consumo
        global inventario_abierto, tienda_abierta, slot_seleccionado, submenu_abierto
        global tiempo_acum_necesidades, tiempo_acum_ingreso, ultimo_anuncio_ts
        global anuncio_activo, inicio_anuncio_ts, anuncio_actual, game_over
        global economic_score, purchases_by_item
        global esperando_decision_compra, item_pendiente_compra, precio_pendiente

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

            # ============================================================
            # ARQUITECTURA DE EVENTOS (Prioridad estricta)
            # ============================================================
            accion_inventario = None
            accion_slot = None
            cerrar_interfaces = False

            events = pygame.event.get()
            
            for event in events:
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

                # ============================================================
                # PRIORIDAD MÁXIMA: Popup de decisión
                # ============================================================
                if popup_decision.activo:
                    if popup_decision.manejar_evento(event):
                        continue  # Consumir evento

                # ============================================================
                # PRIORIDAD 1: Submenu (si está abierto)
                # ============================================================
                if submenu_abierto and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    accion = ui.check_submenu_click(mx, my)
                    
                    if accion == "close":
                        submenu_abierto = False
                        slot_seleccionado = None
                    elif accion == "usar":
                        accion_inventario = "usar"
                        accion_slot = slot_seleccionado
                    elif accion == "vender":
                        accion_inventario = "vender"
                        accion_slot = slot_seleccionado
                    continue

                # ============================================================
                # PRIORIDAD 2: Inventario
                # ============================================================
                if inventario_abierto and not submenu_abierto:
                    handled = ui.handle_event_inventory(event, inventario)
                    if isinstance(handled, tuple):
                        close, slot_idx, submenu = handled
                        if close:
                            cerrar_interfaces = True
                        if slot_idx is not None:
                            slot_seleccionado = slot_idx
                            submenu_abierto = submenu
                    continue

                # ============================================================
                # PRIORIDAD 3: Comparador de productos
                # ============================================================
                if comparador_productos.activo:
                    if comparador_productos.manejar_evento(event):
                        continue

                # ============================================================
                # PRIORIDAD 4: Tienda
                # ============================================================
                if tienda_abierta and not esperando_decision_compra:
                    # Tecla C para abrir comparador
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                        comparador_productos.abrir()
                        continue
        
                    # ✅ FIX: Completar lógica de compra
                    handled = tienda.handle_event(event, dinero, jugador, inventario)
                    if isinstance(handled, tuple):
                        close = handled[0]
                        dinero_delta = handled[1] if len(handled) > 1 else 0
                        consumo_delta = handled[2] if len(handled) > 2 else 0
                        item_name = handled[3] if len(handled) > 3 else None
                        
                        if close:
                            tienda_abierta = False
                            continue
                        
                        # ✅ Interceptar compra para mostrar popup de decisión
                        if item_name and dinero_delta < 0:  # Es una compra
                            print(f"[Main] Interceptando compra de: {item_name}")
                            
                            # Obtener info del producto
                            info_decision = coordinador_anticonsumo.procesar_compra(
                                item_name, 
                                abs(dinero_delta)
                            )
                            
                            # Guardar compra pendiente
                            esperando_decision_compra = True
                            item_pendiente_compra = item_name
                            precio_pendiente = abs(dinero_delta)
                            
                            # Callbacks del popup
                            def confirmar_compra():
                                global dinero, consumo, esperando_decision_compra
                                global item_pendiente_compra, economic_score
                                
                                # Ejecutar compra
                                dinero -= precio_pendiente
                                consumo = min(100.0, consumo + info_decision.get('contaminacion_generada', 0))
                                
                                # Confirmar en coordinador (actualiza contaminación ambiental)
                                coordinador_anticonsumo.confirmar_compra(item_pendiente_compra)
                                
                                # Estadísticas
                                purchases_by_item[item_pendiente_compra] = purchases_by_item.get(item_pendiente_compra, 0) + 1
                                economic_score += 1
                                
                                # Notificación
                                notificaciones.agregar(
                                    f"Compraste: {item_pendiente_compra} (-${precio_pendiente})",
                                    "info", 2500
                                )
                                
                                # Reset estado
                                esperando_decision_compra = False
                                item_pendiente_compra = None
                                
                                print(f"[Main] ✓ Compra confirmada: {item_pendiente_compra}")
                            
                            def cancelar_compra():
                                global esperando_decision_compra, item_pendiente_compra
                                esperando_decision_compra = False
                                item_pendiente_compra = None
                                notificaciones.agregar("Compra cancelada - Decisión consciente", "success", 2000)
                                print("[Main] ✗ Compra cancelada por el jugador")
                            
                            # Abrir popup
                            popup_decision.abrir(
                                producto=item_name,
                                info_decision=info_decision,
                                on_confirmar=confirmar_compra,
                                on_cancelar=cancelar_compra
                            )
                            continue

                # ============================================================
                # PRIORIDAD 5: Teclas globales
                # ============================================================
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
                            estado_mundo = coordinador_anticonsumo.get_estado_mundo()
                            for npc in npc_list:
                                if jugador.rect.colliderect(npc.rect):
                                    resp = npc.responder(jugador, economic_score, estado_mundo)
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
            # EJECUTAR ACCIONES PENDIENTES
            # ============================================================
            if cerrar_interfaces:
                inventario_abierto = False
                slot_seleccionado = None
                submenu_abierto = False

            if accion_inventario and accion_slot is not None:
                if accion_inventario == "usar":
                    if 0 <= accion_slot < len(inventario.contenido):
                        item = inventario.obtener_item(accion_slot)
                        
                        if item:
                            efectos = getattr(item, "effect", {})
                            alimentacion = min(100.0, alimentacion + efectos.get("alimentacion", 0))
                            recreacion = min(100.0, recreacion + efectos.get("recreacion", 0))
                            consumo = min(100.0, consumo + efectos.get("consumo", 0))
                            
                            item_usado = inventario.usar_objeto(accion_slot)
                            
                            if item_usado:
                                msg = f"Usaste: {item.name}"
                                if efectos.get("alimentacion", 0) > 0:
                                    msg += f" (+{int(efectos['alimentacion'])} alim.)"
                                if efectos.get("recreacion", 0) > 0:
                                    msg += f" (+{int(efectos['recreacion'])} recr.)"
                                notificaciones.agregar(msg, "success", 3000)
                            
                            submenu_abierto = False
                            slot_seleccionado = None

                elif accion_inventario == "vender":
                    if 0 <= accion_slot < len(inventario.contenido):
                        item = inventario.obtener_item(accion_slot)
                        
                        if item:
                            precio = getattr(item, "price", 0)
                            item_vendido = inventario.vender_objeto(accion_slot)
                            
                            if item_vendido:
                                dinero += precio
                                notificaciones.agregar(f"Vendiste: {item_vendido.name} (+${precio})", "success", 3000)
                            
                            submenu_abierto = False
                            slot_seleccionado = None

            # ============================================================
            # LÓGICA DEL JUEGO
            # ============================================================
            if estado_actual == JUGANDO and not game_over:
                # Actualizar notificaciones
                notificaciones.actualizar()
                
                # Velocidad penalizada por inventario
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

                # ✅ NUEVO: Actualizar sistemas anti-consumismo
                estado_mundo = coordinador_anticonsumo.get_estado_mundo()
                gestor_impacto_visual.actualizar(dt, estado_mundo['contaminacion'])
                particulas_atmosfera.actualizar(dt, estado_mundo['contaminacion'])
                popup_decision.actualizar(dt)

                # Game over
                if consumo >= 90.0:
                    game_over = True

            # ============================================================
            # RENDERIZADO
            # ============================================================
            if estado_actual == JUGANDO:
                objetivo_x = jugador.rect.centerx - VALUES[0] // 2
                objetivo_y = jugador.rect.centery - VALUES[1] // 2
                objetivo_x = max(0, min(objetivo_x, mapa_rect.width - VALUES[0]))
                objetivo_y = max(0, min(objetivo_y, mapa_rect.height - VALUES[1]))
                lerp_factor = 0.15
                camara.x += (objetivo_x - camara.x) * lerp_factor
                camara.y += (objetivo_y - camara.y) * lerp_factor

            # ---------- MENÚ ----------
            if estado_actual == MENU:
                screen.blit(fondo_menu, (0,0))

            # ---------- JUGANDO ----------
            elif estado_actual == JUGANDO:
                # Fondo del mapa
                screen.blit(fondo_nivel, (-camara.x, -camara.y))

                # ✅ NUEVO: Renderizar basura ANTES del jugador
                gestor_impacto_visual.renderizar_capa_fondo(screen, camara)

                # NPCs
                try:
                    comerciante.dibujar(screen, camara)
                except Exception:
                    pass
                for npc in npc_list:
                    npc.dibujar(screen, camara)

                # Jugador
                try:
                    jugador.dibujar(screen, camara)
                except Exception:
                    pygame.draw.rect(screen, (0,120,255),
                                     (jugador.rect.x - camara.x, jugador.rect.y - camara.y,
                                      jugador.rect.width, jugador.rect.height))

                # Debug colisiones
                sistema_col.dibujar_debug(screen, camara)

                # ✅ NUEVO: Overlay de color grading (filtro ambiental)
                gestor_impacto_visual.renderizar_capa_overlay(screen)

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

                # HUD
                dibujar_hud(screen)
                
                # ✅ NUEVO: Indicador de contaminación (widget circular)
                gestor_impacto_visual.renderizar_ui(screen)

            # ============================================================
            # INTERFACES (siempre encima del mundo)
            # ============================================================
            
            # Inventario
            if inventario_abierto:
                ui.draw_inventory(screen, inventario,
                                     slot_selected=slot_seleccionado,
                                     open_submenu=submenu_abierto)
            
            # Tienda
            if tienda_abierta:
                tienda.draw(screen)
            
            # Submenu del inventario
            if submenu_abierto and slot_seleccionado is not None:
                ui.draw_submenu(screen)

            # ✅ NUEVO: Comparador de productos
            if comparador_productos.activo:
                comparador_productos.dibujar(screen)

            # Diálogo
            if dialogo_en_progreso and dialogo_activo:
                dialogo_activo.actualizar(dt)
                dialogo_activo.dibujar(screen)
                if not dialogo_activo.en_dialogo:
                    dialogo_en_progreso = False
            
            # Notificaciones
            notificaciones.dibujar(screen)

            # ✅ NUEVO: Popup de decisión (máxima prioridad visual)
            if popup_decision.activo:
                popup_decision.dibujar(screen)

            # ✅ NUEVO: Partículas atmosféricas (en niveles críticos)
            particulas_atmosfera.dibujar(screen)

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

    # ====================================================================
    # PUNTO DE ENTRADA
    # ====================================================================
    if __name__ == "__main__":
        main_loop()

except Exception as e:
    print("\n\n#####################################################")
    print("## ERROR CRÍTICO: FALLO AL INICIAR LA APLICACIÓN ##")
    print("#####################################################")
    print(f"Error específico: {e}\n")
    traceback.print_exc()
    print("\n--- DIAGNÓSTICO ---")
    print("Posibles causas:")
    print("1. Falta algún archivo de código (.py) en la misma carpeta")
    print("2. Faltan assets en la carpeta 'assets/'")
    print("3. Versión incompatible de pygame")
    print("\nArchivos necesarios:")
    print("- personaje2.py")
    print("- colisiones.py")
    print("- dialogos.py")
    print("- inventario.py")
    print("- ui.py")
    print("- tienda.py")
    print("- notificaciones.py")
    print("- mecanicas_anticonsumo.py")
    print("- popup_decision.py")
    print("- comparador_productos.py")
    print("- impacto_visual_mundo.py")
    print("------------------")
    input("Presiona ENTER para cerrar...")