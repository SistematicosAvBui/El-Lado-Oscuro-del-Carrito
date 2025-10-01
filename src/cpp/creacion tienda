#include "personaje.h"
#include <iostream>
#include <vector>
#include <memory>
using namespace std;

class Producto {
protected:
    string nombre;
    double precio;
public:
    Producto(string n, double p) : nombre(n), precio(p) {}
    virtual ~Producto() {}
    virtual void mostrar() const {
        cout << "Producto: " << nombre << " | Precio: " << precio << endl;
    }
    virtual double getPrecio() const { return precio; }
    virtual string getNombre() const { return nombre; }
};

class Bien : public Producto {
public:
    Bien(string n, double p) : Producto(n, p) {}
    void mostrar() const override {
        cout << "Bien " << nombre << " | Precio: " << precio << endl;
    }
};

class Servicio : public Producto {
public:
    Servicio(string n, double p) : Producto(n, p) {}
    void mostrar() const override {
        cout << "Servicio -> " << nombre << " | Tarifa: " << precio << endl;
    }
};

class Tienda {
private:
    vector<shared_ptr<Producto>> productos;
    double totalCompras = 0;
public:
    void agregarProducto(shared_ptr<Producto> p) {
        productos.push_back(p);
    }
    void mostrarProductos() {
        cout << "\n--- Lista de productos y servicios disponibles ---\n";
        for (size_t i = 0; i < productos.size(); i++) {
            cout << i + 1 << ". ";
            productos[i]->mostrar();
        }
    }
    void comprarProducto(int indice) {
        if (indice >= 1 && indice <= (int)productos.size()) {
            totalCompras += productos[indice - 1]->getPrecio();
            cout << "Has comprado: " << productos[indice - 1]->getNombre()
                << " por " << productos[indice - 1]->getPrecio() << endl;
        }
        else {
            cout << "Opción no válida.\n";
        }
    }
    void mostrarTotal() const {
        cout << "\nTotal de la compra: " << totalCompras << endl;
    }
};

int main() {
    Tienda tienda;
    tienda.agregarProducto(make_shared<Bien>("Ropa", 50.0));
    tienda.agregarProducto(make_shared<Bien>("Comida", 20.0));
    tienda.agregarProducto(make_shared<Bien>("Agua potable (botella)", 5.0));
    tienda.agregarProducto(make_shared<Servicio>("Servicio de luz", 100.0));
    tienda.agregarProducto(make_shared<Servicio>("Servicio de agua", 80.0));
    tienda.agregarProducto(make_shared<Servicio>("Internet", 120.0));
    int opcion;
    do {
        tienda.mostrarProductos();
        cout << "\nSeleccione un producto/servicio a comprar (0 para salir): ";
        cin >> opcion;
        if (opcion != 0) {
            tienda.comprarProducto(opcion);
        }
    } while (opcion != 0);
    tienda.mostrarTotal();
    return 0;
}
