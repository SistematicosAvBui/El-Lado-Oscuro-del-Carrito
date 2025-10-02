# 🌴 El Lado Oscuro del Carrito

Un juego en **Python + Pygame** con lógica base en **C++ (Pybind11)**.  
El jugador explora una isla, interactúa con NPCs y realiza misiones relacionadas con el cuidado del medio ambiente.  

---

## 🎮 Características
- **Jugador (Protagonista)** con movimiento libre en escenarios.  
- **NPCs dinámicos** que pueden seguir al jugador o asignar misiones.  
- **Sistema de misiones**: recoger basura, interactuar con personajes, obtener recompensas.  
- **Economía simple**: el dinero ganado se usa para progresar y mejorar el entorno.  
- **Foco temático**: concientizar sobre el **consumismo** y la importancia del reciclaje.  

---

## 🛠️ Tecnologías
- **C++** → Lógica de personaje y economía.  
- **Pybind11** → Exposición de clases y métodos de C++ a Python.  
- **Python (Pygame)** → Motor del juego, gráficos, NPCs y jugabilidad.  

---

## 📂 Estructura del proyecto
```
├── src
│   ├── cpp/              # Código C++ base
│   ├── bindings/         # Pybind11 bindings
│   ├── include/          # Headers C++
│   └── python/           # Lógica principal del juego (Pygame)
│
├── assets/               # Sprites y fondos
└── README.md             # Este archivo
```

---

## 🚀 Ejecución
1. Compilar el módulo de C++ con CMake:
   ```bash
   cmake --build . --config Release
   ```
2. Ejecutar el juego desde Python:
   ```bash
   python src/python/pruebas_main.py
   ```

---

## 🎯 Objetivo del juego
El jugador debe explorar la isla, recoger basura y completar misiones para obtener dinero.  
El dinero no está pensado para el consumismo, sino para **restaurar y mejorar el entorno**.  

El mensaje principal:  
> “El consumo sin propósito no trae progreso real. La sostenibilidad sí.”  

---

## 📌 Futuro
- Misiones más variadas.  
- Varios escenarios explorables.  
- Mejoras visuales (sprites con transparencia, animaciones).  
- Sistema de decisiones con impacto ambiental.  

---

👨‍💻 **Autor:** Proyecto académico en desarrollo.  