#include "personaje.h"
#include <iostream>
using namespace std;

Personaje::Personaje(int m, int v) {
    movimiento = m;
    dinero = 1500; // ignoramos v y usamos dinero fijo como en tu ejemplo
}

void Personaje::gasto(int cantidad) {
    if (dinero >= cantidad) {
        dinero -= cantidad;
    }
    else {
        cout << "SIN SALDO" << endl;
    }
}