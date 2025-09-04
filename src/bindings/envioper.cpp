#include <pybind11/pybind11.h>
#include "personaje.h"

namespace py = pybind11;

PYBIND11_MODULE(personaje, m) {
    m.doc() = "Modulo de personaje para el juego del consumismo";

    py::class_<Personaje>(m, "Personaje")
        .def(py::init<int, int>())        // Constructor (m, v)
        .def("gasto", &Personaje::gasto); // M�todo gasto
}