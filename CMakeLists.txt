# Versión mínima de CMake requerida
cmake_minimum_required(VERSION 3.10)

# Nombre del proyecto
project(el_lado_oscuro_del_carrito)

# Configuración del estándar de C++
set(CMAKE_CXX_STANDARD 17)            # Usar C++17
set(CMAKE_CXX_STANDARD_REQUIRED ON)   # Obligatorio, no permite versiones anteriores
set(CMAKE_CXX_EXTENSIONS OFF)         # No usar extensiones del compilador (como GNU extensions)

# Configuración de warnings
if (MSVC)
    # Si usamos Visual Studio, activar nivel 4 de warnings
    add_compile_options(/W4)
else()
    # Para otros compiladores (GCC, Clang), activar warnings comunes y pedantic
    add_compile_options(-Wall -Wextra -pedantic)
endif()

# Añadir subdirectorio de pybind11 (de third_party)
add_subdirectory(third_party/pybind11)

# Incluir directorios de encabezados
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/third_party/pybind11/include)  # pybind11
include_directories(src/include)                                               # directorio propio con headers

# Lista de archivos fuente para el módulo personaje
set(PERSONAJE_SOURCES
    src/cpp/personaje.cpp
    src/bindings/envioper.cpp
)

# Crear módulo Python usando pybind11
pybind11_add_module(personaje ${PERSONAJE_SOURCES})

# Configuración de la carpeta de salida de los módulos compilados
set(PYTHON_MODULE_OUTPUT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/compilados_py)  # Carpeta compilados_py/

# Indicar que el módulo personaje debe generarse dentro de compilados_py
set_target_properties(personaje PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${PYTHON_MODULE_OUTPUT_DIR}   # Para sistemas tipo Unix (.so)
    RUNTIME_OUTPUT_DIRECTORY ${PYTHON_MODULE_OUTPUT_DIR}   # Para Windows (.pyd)
)

