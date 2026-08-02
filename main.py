print("=== Sistema de Inventario para Restaurantes ===")

inventario = []

while True:
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Agregar producto")
    print("2. Ver inventario")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        producto = input("Nombre del producto: ")
        cantidad = input("Cantidad disponible: ")

        inventario.append({
            "nombre": producto,
            "cantidad": cantidad
        })

        print("Producto agregado correctamente.")

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