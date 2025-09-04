#include <iostream>
#include <stdlib.h>
using namespace std;

class mision {
private:
    string nombre;
    string descripcion;
    int recompensa;
    bool completada;

public:
    mision(string  d, string n, int r) {
        nombre = n;
        descripcion = d;
        recompensa = r;
        completada = false;
    }
    void mostrarmision() {

        cout << "Mision: " << nombre << endl;
        cout << "Descripcion :" << descripcion << endl;
        cout << "Recompensa: " << recompensa << endl;
        cout << "Estado: " << (completada ? "Completada" : "No completada") << endl;
    }

    int completar() {
        if (!completada) {
            completada = true;
            return recompensa; // parte mas importante ya que devuelve los puntasos al player (ojo importante el manejo)
        }
        else {
            cout << "Ya habías completado esta misión." << endl;
            return 0;
        }
    }

    bool preguntafinal() {

        return completada;
    }
};


int main (){
    mision m1("No comprar innecesario", "Ignora una tentación de compra", 89);
    m1.mostrarmision();

    int puntos = m1.completar();
    cout << "dinero ganado : " << puntos << endl;

    m1.mostrarmision();

    mision m2("Elige lo necesario sobre lo extra", "Entre dos opciones, escoger solo lo útil", 57);
    m2.mostrarmision();

    puntos += m2.completar();
    cout << "dinero ganado : " << puntos << endl;

    m2.mostrarmision();


    return 0;
}