# inventario.py - VERSIÓN CORREGIDA
import pygame

class Inventario:
    def __init__(self, capacidad):
        """
        Inventario mejorado con validaciones.
        capacidad = espacios totales (10 slots por defecto)
        """
        self.contenido = []  # lista de Item (objetos)
        self.capacidad_maxima = capacidad
        self.capacidad = capacidad  # espacios libres actuales

    def abrir_inventario(self, pantalla, interfaz):
        """Compatibilidad: interfaz tiene draw_inventory"""
        return interfaz.interfaz_inventario(pantalla, self.capacidad)

    def agregar_objeto(self, producto):
        """
        FIX: Validación mejorada de espacios
        """
        if self.capacidad <= 0:
            print("[Inventario] Sin espacio disponible")
            return False
        
        if len(self.contenido) >= self.capacidad_maxima:
            print("[Inventario] Inventario lleno")
            return False
        
        self.contenido.append(producto)
        self.capacidad -= 1
        print(f"[Inventario] Agregado: {producto.name}")
        return True

    def vender_objeto(self, index):
        """
        FIX: Validación de índice antes de acceder
        """
        if not self._validar_indice(index):
            print(f"[Inventario] Índice inválido para vender: {index}")
            return None
        
        item = self.contenido.pop(index)
        self.capacidad += 1
        print(f"[Inventario] Vendido: {item.name}")
        return item

    def usar_objeto(self, index):
        """
        FIX: Validación de índice antes de acceder
        """
        if not self._validar_indice(index):
            print(f"[Inventario] Índice inválido para usar: {index}")
            return None
        
        item = self.contenido.pop(index)
        self.capacidad += 1
        print(f"[Inventario] Usado: {item.name}")
        return item

    def obtener_item(self, index):
        """
        NUEVO: Obtener item sin eliminarlo (para preview)
        """
        if self._validar_indice(index):
            return self.contenido[index]
        return None

    def _validar_indice(self, index):
        """
        NUEVO: Validación centralizada de índices
        """
        return 0 <= index < len(self.contenido)

    def esta_lleno(self):
        """NUEVO: Helper para verificar si está lleno"""
        return self.capacidad <= 0

    def espacios_usados(self):
        """NUEVO: Cantidad de slots ocupados"""
        return len(self.contenido)

    def __len__(self):
        """NUEVO: Permite usar len(inventario)"""
        return len(self.contenido)

    def __repr__(self):
        """NUEVO: Representación para debug"""
        return f"<Inventario: {len(self.contenido)}/{self.capacidad_maxima} items>"