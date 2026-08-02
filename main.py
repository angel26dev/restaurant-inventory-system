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
    print("3. Buscar producto")
    print("4. Eliminar producto")
    print("5. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        producto = input("Nombre del producto: ")
        cantidad = input("Cantidad disponible: ")
        precio = float(input("Precio del producto: "))

        nuevo_producto = {
            "nombre": producto,
            "cantidad": cantidad,
            "precio": precio
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
                   producto["cantidad"],
                   "| Precio: $",
                   producto["precio"]
)
    elif opcion == "3":
        nombre = input("Ingrese el nombre del producto a buscar: ")

        encontrado = False 

        for producto in inventario:
            if producto["nombre"].lower() == nombre.lower():

              print("\n===PRODUCTO ENCONTRADO===")    
              print("Nombre:",       producto["nombre"])    
              print("Cantidad:",     producto["cantidad"]
              print("Precio: $",
producto["precio"])                   
               print("==========================")
                     
                encontrado = True
                break

        if not encontrado: 
            print("No se encontró ese producto.")

    elif opcion == "4":
        nombre = input("Ingrese el nombre del producto a eliminar: ")

        encontrado = False

        for producto in inventario:
            if producto["nombre"].lower() == nombre.lower():
                inventario.remove(producto)
                guardar_inventario(inventario)
                print("Producto eliminado correctamente.")
                encontrado = True
                break

        if not encontrado:
            print("No se encontró ese producto.")


    elif opcion == "5":
        print("Cerrando sistema...")
        break

    else:
        print("Opción no válida.")