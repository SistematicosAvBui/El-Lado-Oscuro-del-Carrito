#ifndef PERSONAJE_H
#define PERSONAJE_H

class Personaje {
private:
    int movimiento;
    int dinero;

public:
    Personaje(int m, int v);

    void gasto(int cantidad);
};

#endif