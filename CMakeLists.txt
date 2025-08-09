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

# Carpeta con archivos .h/.hpp
include_directories(src/include)

# Guardar rutas de los .cpp
file(GLOB_RECURSE CPP_SOURCES src/cpp/*.cpp)
file(GLOB_RECURSE BINDINGS_SOURCES src/bindings/*.cpp)

