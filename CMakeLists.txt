cmake_minimum_required(VERSION 3.10)  # Versión mínima de CMake
project(el_lado_oscuro_del_carrito)   # Nombre del proyecto

set(CMAKE_CXX_STANDARD 17)            # Usar C++17
set(CMAKE_CXX_STANDARD_REQUIRED ON)   # Obligatorio
set(CMAKE_CXX_EXTENSIONS OFF)         # Sin extensiones del compilador

# Warnings
if (MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -pedantic)
endif()

# Añadir pybind11 desde third_party
add_subdirectory(third_party/pybind11)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/third_party/pybind11/include)

# Carpeta con archivos .h/.hpp
include_directories(src/include)

set(PERSONAJE_SOURCES
    src/cpp/personaje.cpp
    src/bindings/envioper.cpp
)
# Crear módulo pybind11 SOLO para personaje
pybind11_add_module(personaje ${PERSONAJE_SOURCES})

