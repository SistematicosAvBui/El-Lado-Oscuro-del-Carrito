cmake_minimum_required(VERSION 3.10)
project(el_lado_oscuro_del_carrito)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if (MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -pedantic)
endif()

add_subdirectory(third_party/pybind11)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/third_party/pybind11/include)
include_directories(src/include)

set(PERSONAJE_SOURCES
    src/cpp/personaje.cpp
    src/bindings/envioper.cpp
)

# Crear módulo pybind11
pybind11_add_module(personaje ${PERSONAJE_SOURCES})

# Carpeta de salida para los módulos Python
set(PYTHON_MODULE_OUTPUT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/compilados_py)
set_target_properties(personaje PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${PYTHON_MODULE_OUTPUT_DIR}
    RUNTIME_OUTPUT_DIRECTORY ${PYTHON_MODULE_OUTPUT_DIR}
)

