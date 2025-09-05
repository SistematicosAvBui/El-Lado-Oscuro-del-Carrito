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

        // Propiedad movimiento
        .def_property("movimiento",
            [](const Personaje& p) { return p.movimiento; },
            [](Personaje& p, int value) { p.movimiento = value; },
            "Atributo que representa el movimiento del personaje")

        // Propiedad dinero
        .def_property("dinero",
            [](const Personaje& p) { return p.dinero; },
            [](Personaje& p, int value) { p.dinero = value; },
            "Cantidad de dinero del personaje");
}