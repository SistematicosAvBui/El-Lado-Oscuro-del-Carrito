#include <pybind11/pybind11.h>
#include "personaje.h"

namespace py = pybind11;

PYBIND11_MODULE(personaje, m) {
    m.doc() = "Módulo de Personaje expuesto con Pybind11";

    py::class_<Personaje>(m, "Personaje")
        // Constructor
        .def(py::init<int, int>(), py::arg("movimiento"), py::arg("dinero"))

        // Método gasto
        .def("gasto", &Personaje::gasto, py::arg("cantidad"),
            "Descuenta una cantidad de dinero si hay saldo suficiente")

        // Atributos expuestos directamente
        .def_readwrite("movimiento", &Personaje::movimiento,
            "Atributo público que representa el movimiento del personaje")
        .def_readwrite("dinero", &Personaje::dinero,
            "Cantidad de dinero del personaje");
}