#ifndef PERSONAJE_H
#define PERSONAJE_H

class Personaje {
public:
    int movimiento;
    int dinero;

    Personaje(int m, int v);

    void gasto(int cantidad);
};

#endif