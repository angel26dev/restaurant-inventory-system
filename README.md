# 🍽️ Restaurant Inventory System

Un sistema de gestión de inventario y control de almacén para restaurantes desarrollado en Python. A diferencia de los sistemas tradicionales que descuentan insumos mediante recetas teóricas, este sistema implementa un **control de stock basado en flujo real de almacén** (entradas por compras y salidas por despachos a cocina).

---

## 🎯 Problema de Negocio que Resuelve

En la industria gastronómica, intentar descontar inventario automáticamente plato por plato mediante recetas teóricas falla debido a:
- Porcionado "al ojo" en momentos de alta demanda.
- Mermas no registradas durante la preparación.
- Pruebas de menú y ajustes del chef.

Este sistema soluciona el desfase financiero permitiendo registrar las **entradas por factura** y las **salidas reales enviadas a cocina**, generando auditorías precisas sobre el consumo real.

---

## 🚀 Funcionalidades Principales

- **Gestión de Insumos:** Registro de productos con nombre, cantidad, precio unitario y límite de stock mínimo.
- **Control de Almacén:**
  - **Entradas:** Suma de mercancía recibida por proveedores.
  - **Salidas:** Despacho de insumos hacia el área de cocina.
- **Alertas de Bajo Stock ⚠️:** Notificaciones automáticas cuando un insumo alcanza su límite crítico.
- **Búsqueda Flexible:** Algoritmo de búsqueda por coincidencia parcial de texto.
- **Persistencia de Datos:** Almacenamiento local automático en formato JSON.

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **JSON** (para el almacenamiento de datos)

---

## 📌 Próximos Pasos en el Desarrollo

- [ ] Integración con comandera/POS para auditoría de rendimiento (Mermas vs. Ventas).
- [ ] Exportación de reportes de compras necesarias.
- [ ] Interfaz gráfica (GUI) o versión Web.
