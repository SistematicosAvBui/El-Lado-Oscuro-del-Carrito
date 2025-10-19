# mecanicas_anticonsumo.py
"""
Sistema central de mecánicas anti-consumismo.
Coordina la interacción entre todos los subsistemas educativos del juego.

Principios SOLID aplicados:
- SRP: Cada clase tiene una responsabilidad única
- OCP: Extensible sin modificar código existente
- LSP: Interfaces consistentes
- ISP: Interfaces específicas por funcionalidad
- DIP: Depende de abstracciones, no implementaciones concretas
"""

import pygame
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# ====================================================================
# ENUMERACIONES Y TIPOS
# ====================================================================

class TipoProducto(Enum):
    """Clasificación de productos según su impacto en el consumismo"""
    NECESIDAD_BASICA = "necesidad_basica"  # Comida, agua
    NECESIDAD_MEDIA = "necesidad_media"    # Herramientas, ropa
    DESEO_LEVE = "deseo_leve"              # Entretenimiento básico
    DESEO_FUERTE = "deseo_fuerte"          # Lujos, tecnología innecesaria
    
class ImpactoAmbiental(Enum):
    """Nivel de impacto ecológico de un producto"""
    BAJO = "bajo"
    MEDIO = "medio"
    ALTO = "alto"
    MUY_ALTO = "muy_alto"

# ====================================================================
# DATA CLASSES
# ====================================================================

@dataclass
class ProductoExtendido:
    """
    Extensión de la clase Item con atributos anti-consumismo.
    
    Atributos:
        tipo: Clasificación del producto (necesidad/deseo)
        impacto: Nivel de contaminación que genera
        durabilidad: Cuánto dura el producto (0-100)
        mensaje_reflexion: Texto personalizado para el popup
    """
    tipo: TipoProducto
    impacto: ImpactoAmbiental
    durabilidad: int = 100
    mensaje_reflexion: str = ""
    
    def get_valor_contaminacion(self) -> int:
        """Retorna cuánto contamina este producto (0-15)"""
        mapping = {
            TipoProducto.NECESIDAD_BASICA: 1,
            TipoProducto.NECESIDAD_MEDIA: 3,
            TipoProducto.DESEO_LEVE: 8,
            TipoProducto.DESEO_FUERTE: 15
        }
        return mapping.get(self.tipo, 5)
    
    def get_color_impacto(self) -> Tuple[int, int, int]:
        """Retorna color RGB según impacto ambiental"""
        colores = {
            ImpactoAmbiental.BAJO: (80, 220, 80),
            ImpactoAmbiental.MEDIO: (255, 200, 60),
            ImpactoAmbiental.ALTO: (255, 140, 60),
            ImpactoAmbiental.MUY_ALTO: (255, 80, 80)
        }
        return colores.get(self.impacto, (200, 200, 200))

# ====================================================================
# GESTOR DE IMPACTO AMBIENTAL
# ====================================================================

class GestorImpactoAmbiental:
    """
    Gestiona el nivel de contaminación del mundo y sus consecuencias.
    
    Responsabilidades:
    - Calcular contaminación acumulada
    - Determinar thresholds de impacto
    - Proporcionar feedback visual/textual
    """
    
    def __init__(self):
        self.contaminacion = 0.0  # 0-100
        self.umbral_advertencia = 30
        self.umbral_critico = 60
        self.umbral_colapso = 85
        
        # Efectos visuales según nivel
        self.efectos_activos = {
            "basura_visible": False,
            "filtro_gris": False,
            "npcs_preocupados": False,
            "crisis_ambiental": False
        }
    
    def agregar_contaminacion(self, cantidad: float):
        """Aumenta la contaminación (máx 100)"""
        self.contaminacion = min(100.0, self.contaminacion + cantidad)
        self._actualizar_efectos()
        print(f"[Impacto Ambiental] Contaminación: {self.contaminacion:.1f}%")
    
    def reducir_contaminacion(self, cantidad: float):
        """Reduce la contaminación (acciones sostenibles)"""
        self.contaminacion = max(0.0, self.contaminacion - cantidad)
        self._actualizar_efectos()
    
    def _actualizar_efectos(self):
        """Actualiza los efectos visuales según el nivel de contaminación"""
        nivel = self.contaminacion
        
        self.efectos_activos["basura_visible"] = nivel >= self.umbral_advertencia
        self.efectos_activos["filtro_gris"] = nivel >= self.umbral_critico
        self.efectos_activos["npcs_preocupados"] = nivel >= self.umbral_critico
        self.efectos_activos["crisis_ambiental"] = nivel >= self.umbral_colapso
    
    def get_nivel_contaminacion(self) -> str:
        """Retorna descripción textual del nivel"""
        if self.contaminacion < self.umbral_advertencia:
            return "Bajo"
        elif self.contaminacion < self.umbral_critico:
            return "Moderado"
        elif self.contaminacion < self.umbral_colapso:
            return "Alto"
        else:
            return "Crítico"
    
    def get_color_indicador(self) -> Tuple[int, int, int]:
        """Color del indicador de contaminación"""
        if self.contaminacion < self.umbral_advertencia:
            return (80, 220, 80)
        elif self.contaminacion < self.umbral_critico:
            return (255, 200, 60)
        elif self.contaminacion < self.umbral_colapso:
            return (255, 140, 60)
        else:
            return (255, 80, 80)
    
    def get_overlay_alpha(self) -> int:
        """Alpha del overlay gris (0-150)"""
        if not self.efectos_activos["filtro_gris"]:
            return 0
        # Interpolación: 60% → 0 alpha, 100% → 150 alpha
        ratio = (self.contaminacion - self.umbral_critico) / (100 - self.umbral_critico)
        return int(ratio * 150)
    
    def debe_generar_basura(self) -> bool:
        """Determina si debe aparecer basura en el mapa"""
        return self.efectos_activos["basura_visible"]
    
    def get_dialogo_npc_ambiental(self, npc_role: str) -> Optional[str]:
        """
        Retorna diálogo alternativo si la contaminación es alta.
        Retorna None si no hay cambio.
        """
        if not self.efectos_activos["npcs_preocupados"]:
            return None
        
        dialogos = {
            "vendedor": "Las ventas van bien... pero el aire se siente pesado.",
            "consumista": "¿Notaste que hay más basura en las calles últimamente?",
            "inversor": "La economía crece, pero el planeta sufre. ¿Vale la pena?",
            "civil": "Mis hijos preguntan por qué el cielo está tan gris..."
        }
        
        return dialogos.get(npc_role, "El mundo no se ve igual que antes...")

# ====================================================================
# BASE DE DATOS DE PRODUCTOS EXTENDIDOS
# ====================================================================

class BaseDatosProductos:
    """
    Almacena metadatos de productos para mecánicas anti-consumismo.
    
    Patrón: Repository Pattern
    - Centraliza la información de productos
    - Fácil de extender con nuevos productos
    - Desacoplado de la lógica de negocio
    """
    
    def __init__(self):
        self.productos: Dict[str, ProductoExtendido] = {}
        self._inicializar_productos()
    
    def _inicializar_productos(self):
        """Define los metadatos de cada producto del juego"""
        
        # NECESIDADES BÁSICAS
        self.productos["Manzana"] = ProductoExtendido(
            tipo=TipoProducto.NECESIDAD_BASICA,
            impacto=ImpactoAmbiental.BAJO,
            durabilidad=1,  # Se consume de inmediato
            mensaje_reflexion="La comida es esencial para vivir. Es una necesidad real."
        )
        
        self.productos["Galleta"] = ProductoExtendido(
            tipo=TipoProducto.DESEO_LEVE,
            impacto=ImpactoAmbiental.MEDIO,
            durabilidad=1,
            mensaje_reflexion="¿Realmente tienes hambre o solo antojo de algo dulce?"
        )
        
        self.productos["Libro"] = ProductoExtendido(
            tipo=TipoProducto.NECESIDAD_MEDIA,
            impacto=ImpactoAmbiental.BAJO,
            durabilidad=100,
            mensaje_reflexion="El conocimiento es valioso y este libro durará años."
        )
        
        # DESEOS / LUJOS
        self.productos["Celular"] = ProductoExtendido(
            tipo=TipoProducto.DESEO_FUERTE,
            impacto=ImpactoAmbiental.MUY_ALTO,
            durabilidad=80,
            mensaje_reflexion="¿Necesitas otro celular? La tecnología consume recursos valiosos."
        )
        
        self.productos["Tablet"] = ProductoExtendido(
            tipo=TipoProducto.DESEO_FUERTE,
            impacto=ImpactoAmbiental.MUY_ALTO,
            durabilidad=80,
            mensaje_reflexion="Una tablet más no te hará más feliz. ¿Ya tienes otros dispositivos?"
        )
    
    def get_info(self, nombre_producto: str) -> Optional[ProductoExtendido]:
        """Obtiene metadatos de un producto"""
        return self.productos.get(nombre_producto)
    
    def agregar_producto(self, nombre: str, info: ProductoExtendido):
        """Registra un nuevo producto (extensibilidad)"""
        self.productos[nombre] = info
    
    def get_todos_comparables(self) -> List[Tuple[str, ProductoExtendido]]:
        """Retorna todos los productos para la tabla comparativa"""
        return list(self.productos.items())

# ====================================================================
# COORDINADOR PRINCIPAL
# ====================================================================

class CoordinadorAntiConsumo:
    """
    Coordinador central de todas las mecánicas anti-consumismo.
    
    Patrón: Facade Pattern
    - Simplifica la interacción con múltiples subsistemas
    - Proporciona una interfaz única y coherente
    - Facilita la extensión futura
    """
    
    def __init__(self):
        self.gestor_impacto = GestorImpactoAmbiental()
        self.base_datos = BaseDatosProductos()
    
    def procesar_compra(self, nombre_producto: str, precio: int) -> Dict:
        """
        Procesa una compra y retorna información para el popup.
        
        Returns:
            Dict con:
            - tipo: TipoProducto
            - impacto: ImpactoAmbiental
            - mensaje: str (texto reflexivo)
            - contaminacion_generada: int
        """
        info = self.base_datos.get_info(nombre_producto)
        
        if not info:
            # Producto no registrado, asumir deseo leve
            info = ProductoExtendido(
                tipo=TipoProducto.DESEO_LEVE,
                impacto=ImpactoAmbiental.MEDIO,
                mensaje_reflexion="¿Realmente necesitas esto?"
            )
        
        contaminacion = info.get_valor_contaminacion()
        
        return {
            "tipo": info.tipo,
            "impacto": info.impacto,
            "mensaje": info.mensaje_reflexion,
            "contaminacion_generada": contaminacion,
            "color_impacto": info.get_color_impacto()
        }
    
    def confirmar_compra(self, nombre_producto: str):
        """
        Ejecuta las consecuencias de confirmar una compra.
        """
        info = self.base_datos.get_info(nombre_producto)
        if info:
            contaminacion = info.get_valor_contaminacion()
            self.gestor_impacto.agregar_contaminacion(contaminacion)
            print(f"[AntiConsumo] Compra confirmada: {nombre_producto} (+{contaminacion} contaminación)")
    
    def get_estado_mundo(self) -> Dict:
        """Retorna el estado actual del mundo para renderizado"""
        return {
            "contaminacion": self.gestor_impacto.contaminacion,
            "nivel": self.gestor_impacto.get_nivel_contaminacion(),
            "color": self.gestor_impacto.get_color_indicador(),
            "efectos": self.gestor_impacto.efectos_activos,
            "overlay_alpha": self.gestor_impacto.get_overlay_alpha()
        }
    
    def get_dialogo_npc(self, npc_role: str) -> Optional[str]:
        """Obtiene diálogo alternativo para NPC según contaminación"""
        return self.gestor_impacto.get_dialogo_npc_ambiental(npc_role)
    
    def accion_sostenible(self, tipo: str):
        """
        Premia acciones sostenibles reduciendo contaminación.
        
        Args:
            tipo: "reciclaje", "reparacion", "reutilizacion"
        """
        reduccion = {
            "reciclaje": 5,
            "reparacion": 8,
            "reutilizacion": 3
        }.get(tipo, 2)
        
        self.gestor_impacto.reducir_contaminacion(reduccion)
        print(f"[AntiConsumo] Acción sostenible: {tipo} (-{reduccion} contaminación)")