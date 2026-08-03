from contextlib import asynccontextmanager
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import crear_db_y_tablas, obtener_sesion
from models import MovimientoKardex, Producto, RolUsuario, TipoMovimiento, Usuario


# Evento de arranque: garantiza que las tablas existan al encender el servidor
@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()
    yield


app = FastAPI(
    title="Restaurant Inventory API 🍽️",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def inicio():
    return {"mensaje": "API de Inventario de Restaurante activa 🚀"}


# 1. Crear un producto en el catálogo
@app.post(
    "/productos/",
    response_model=Producto,
    status_code=status.HTTP_201_CREATED,
)
def crear_producto(
    producto: Producto, session: Session = Depends(obtener_sesion)
):
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


# 2. Consultar el inventario completo
@app.get("/productos/", response_model=List[Producto])
def listar_productos(session: Session = Depends(obtener_sesion)):
    productos = session.exec(select(Producto)).all()
    return productos


# 3. REGISTRO DE MOVIMIENTOS (Entrada/Salida) + Auditoría Kardex
@app.post("/movimientos/", response_model=MovimientoKardex)
def registrar_movimiento(
    producto_id: int,
    usuario_id: int,
    tipo: TipoMovimiento,
    cantidad: float,
    motivo: str = None,
    session: Session = Depends(obtener_sesion),
):
    # a. Verificar existencia de entidades
    producto = session.get(Producto, producto_id)
    usuario = session.get(Usuario, usuario_id)

    if not producto:
        raise HTTPException(
            status_code=404, detail="El producto no existe en almacén."
        )
    if not usuario:
        raise HTTPException(
            status_code=404, detail="El usuario indicado no existe."
        )

    cantidad_anterior = producto.cantidad_actual

    # b. Lógica de Negocio: Calcular el nuevo stock según el tipo de operación
    if tipo in [TipoMovimiento.SALIDA_COCINA, TipoMovimiento.MERMA]:
        if producto.cantidad_actual < cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente. Disponible: {producto.cantidad_actual} {producto.unidad_medida}",
            )
        cantidad_nueva = cantidad_anterior - cantidad

    elif tipo in [TipoMovimiento.ENTRADA, TipoMovimiento.AJUSTE]:
        cantidad_nueva = cantidad_anterior + cantidad

    # c. Actualizar el producto y crear la auditoría Kardex de forma atómica
    producto.cantidad_actual = cantidad_nueva

    movimiento = MovimientoKardex(
        producto_id=producto_id,
        usuario_id=usuario_id,
        tipo_movimiento=tipo,
        cantidad=cantidad,
        cantidad_anterior=cantidad_anterior,
        cantidad_nueva=cantidad_nueva,
        motivo=motivo,
    )

    session.add(producto)
    session.add(movimiento)
    session.commit()
    session.refresh(movimiento)

    return movimiento 

# 4. Crear un usuario (Cocinero o Admin)
@app.post(
    "/usuarios/",
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED,
)
def crear_usuario(
    usuario: Usuario, session: Session = Depends(obtener_sesion)
):
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


# 5. Listar usuarios registrados
@app.get("/usuarios/", response_model=List[Usuario])
def listar_usuarios(session: Session = Depends(obtener_sesion)):
    usuarios = session.exec(select(Usuario)).all()
    return usuarios 