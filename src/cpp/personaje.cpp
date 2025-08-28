#include <iostream>
#include <stdlib.h>
using namespace std;

class personaje {
private:
    int movimiento;
    int dinero;

public:
    personaje(int m, int v) {
        movimiento = m;
        dinero = 1500;
    }

    void gasto(int cantidad) {
        if (dinero >= cantidad) {
            dinero -= cantidad;
        }
        else {
            cout << "SIN SALDO" << endl;
        }
    }
};

int main() {
    personaje heroe(5, 100);

    return 0;
}
