import json

ARCHIVO = "inventario.json"


def cargar_inventario():
    try:
        with open(ARCHIVO, "r") as archivo:
            return json.load(archivo)
    except:
        return []


def guardar_inventario(inventario):
    with open(ARCHIVO, "w") as archivo:
        json.dump(inventario, archivo, indent=4)


print("=== Sistema de Inventario para Restaurantes ===")

inventario = cargar_inventario()

while True:
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Agregar producto")
    print("2. Ver inventario")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        producto = input("Nombre del producto: ")
        cantidad = input("Cantidad disponible: ")

        nuevo_producto = {
            "nombre": producto,
            "cantidad": cantidad
        }

        inventario.append(nuevo_producto)

        guardar_inventario(inventario)

        print("Producto guardado correctamente.")

    elif opcion == "2":
        print("\n--- INVENTARIO ACTUAL ---")

        if len(inventario) == 0:
            print("El inventario está vacío.")
        else:
            for producto in inventario:
                print(
                    "Producto:",
                    producto["nombre"],
                    "| Cantidad:",
                    producto["cantidad"]
                )

    elif opcion == "3":
        print("Cerrando sistema...")
        break

    else:
        print("Opción no válida.")