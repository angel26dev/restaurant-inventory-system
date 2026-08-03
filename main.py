import json

ARCHIVO = "inventario.json"


def cargar_inventario():
    try:
        with open(ARCHIVO, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_inventario(inventario):
    with open(ARCHIVO, "w") as archivo:
        json.dump(inventario, archivo, indent=4)


def buscar_producto_por_nombre(inventario, nombre_buscar):
    """Devuelve una lista de productos que coincidan parcialmente con el nombre."""
    coincidencias = []
    for prod in inventario:
        if nombre_buscar.lower() in prod["nombre"].lower():
            coincidencias.append(prod)
    return coincidencias


print("=== Sistema de Inventario para Restaurantes ===")

inventario = cargar_inventario()

while True:
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Registrar nuevo producto")
    print("2. Ver inventario completo")
    print("3. Buscar producto")
    print("4. Ingreso de mercancía (Entrada a almacén)")
    print("5. Salida de mercancía (Despacho a cocina)")
    print("6. Ver alertas de Bajo Stock ⚠️")
    print("7. Eliminar producto")
    print("8. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = input("Nombre del producto: ").strip()
        try:
            cantidad = float(input("Cantidad inicial disponible: "))
            precio = float(input("Precio unitario ($): "))
            stock_minimo = float(
                input("Definir Stock Mínimo para alertas: ")
            )
        except ValueError:
            print("❌ Error: Ingrese valores numéricos válidos.")
            continue

        nuevo_producto = {
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
            "stock_minimo": stock_minimo,
        }

        inventario.append(nuevo_producto)
        guardar_inventario(inventario)
        print(f"✅ Producto '{nombre}' registrado correctamente.")

    elif opcion == "2":
        print("\n--- INVENTARIO ACTUAL ---")
        if not inventario:
            print("El inventario está vacío.")
        else:
            for p in inventario:
                alerta = (
                    " ⚠️ [BAJO STOCK]"
                    if p["cantidad"] <= p["stock_minimo"]
                    else ""
                )
                print(
                    f"• {p['nombre']} | Cantidad: {p['cantidad']} | Precio: ${p['precio']:.2f} | Min: {p['stock_minimo']}{alerta}"
                )

    elif opcion == "3":
        busqueda = input(
            "Ingrese el nombre (o parte del nombre) del producto: "
        ).strip()
        resultados = buscar_producto_por_nombre(inventario, busqueda)

        if resultados:
            print(f"\n=== RESULTADOS ENCONTRADOS ({len(resultados)}) ===")
            for p in resultados:
                alerta = (
                    " ⚠️ [BAJO STOCK]"
                    if p["cantidad"] <= p["stock_minimo"]
                    else ""
                )
                print(
                    f"Nombre: {p['nombre']} | Cantidad: {p['cantidad']} | Precio: ${p['precio']:.2f}{alerta}"
                )
            print("==========================================")
        else:
            print("❌ No se encontraron productos con esa búsqueda.")

    elif opcion == "4":
        # INGRESO DE MERCANCÍA (COMPRAS)
        busqueda = input(
            "Ingrese el nombre del producto que ingresa al almacén: "
        ).strip()
        resultados = buscar_producto_por_nombre(inventario, busqueda)

        if not resultados:
            print("❌ Producto no encontrado. Debe registrarlo primero en la Opción 1.")
        else:
            # Seleccionar el primer producto encontrado
            producto = resultados[0]
            try:
                ingreso = float(
                    input(
                        f"Cantidad a ingresar para '{producto['nombre']}' (Actual: {producto['cantidad']}): "
                    )
                )
                producto["cantidad"] += ingreso
                guardar_inventario(inventario)
                print(
                    f"✅ Ingreso registrado. Nueva cantidad de '{producto['nombre']}': {producto['cantidad']}"
                )
            except ValueError:
                print("❌ Cantidad inválida.")

    elif opcion == "5":
        # SALIDA DE MERCANCÍA (DESPACHO A COCINA)
        busqueda = input(
            "Ingrese el nombre del producto que sale hacia la cocina: "
        ).strip()
        resultados = buscar_producto_por_nombre(inventario, busqueda)

        if not resultados:
            print("❌ Producto no encontrado.")
        else:
            producto = resultados[0]
            try:
                salida = float(
                    input(
                        f"Cantidad a retirar para '{producto['nombre']}' (Disponible: {producto['cantidad']}): "
                    )
                )
                if salida > producto["cantidad"]:
                    print(
                        "❌ Error: No hay suficiente stock en almacén para realizar este despacho."
                    )
                else:
                    producto["cantidad"] -= salida
                    guardar_inventario(inventario)
                    print(
                        f"✅ Salida registrada. Stock restante de '{producto['nombre']}': {producto['cantidad']}"
                    )

                    # Verificar si cayó en stock mínimo
                    if producto["cantidad"] <= producto["stock_minimo"]:
                        print(
                            f"⚠️ ALERTA: El producto '{producto['nombre']}' ha alcanzado el nivel de bajo stock!"
                        )
            except ValueError:
                print("❌ Cantidad inválida.")

    elif opcion == "6":
        # LISTA DE BAJO STOCK
        print("\n--- PRODUCTOS QUE REQUIEREN REABASTECIMIENTO ---")
        bajo_stock = [
            p for p in inventario if p["cantidad"] <= p["stock_minimo"]
        ]

        if not bajo_stock:
            print("✨ Todo está correcto. Ningún producto está en bajo stock.")
        else:
            for p in bajo_stock:
                print(
                    f"🔴 {p['nombre']} -> Actual: {p['cantidad']} | Mínimo requerido: {p['stock_minimo']}"
                )

    elif opcion == "7":
        nombre = input("Ingrese el nombre exacto del producto a eliminar: ").strip()
        encontrado = False

        for p in inventario:
            if p["nombre"].lower() == nombre.lower():
                inventario.remove(p)
                guardar_inventario(inventario)
                print(f"✅ Producto '{p['nombre']}' eliminado del sistema.")
                encontrado = True
                break

        if not encontrado:
            print("❌ No se encontró ese producto.")

    elif opcion == "8":
        print("Cerrando el sistema de inventario...")
        break

    else:
        print("Opción no válida. Intente de nuevo.")
