from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class RolUsuario(str, Enum):
    ADMIN = "admin"
    COCINA = "cocina"


class TipoMovimiento(str, Enum):
    ENTRADA = "ENTRADA"
    SALIDA_COCINA = "SALIDA_COCINA"
    MERMA = "MERMA"
    AJUSTE = "AJUSTE"


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(unique=True, index=True)
    password_hash: str
    rol: RolUsuario = Field(default=RolUsuario.COCINA)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

    movimientos: List["MovimientoKardex"] = Relationship(
        back_populates="usuario"
    )


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    unidad_medida: str
    cantidad_actual: float = Field(default=0.0)
    precio_unitario: float = Field(default=0.0)
    stock_minimo: float = Field(default=0.0)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)

    movimientos: List["MovimientoKardex"] = Relationship(
        back_populates="producto"
    )


class MovimientoKardex(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id")
    usuario_id: int = Field(foreign_key="usuario.id")
    tipo_movimiento: TipoMovimiento
    cantidad: float
    cantidad_anterior: float
    cantidad_nueva: float
    motivo: Optional[str] = None
    fecha_hora: datetime = Field(default_factory=datetime.utcnow)

    producto: Optional[Producto] = Relationship(back_populates="movimientos")
    usuario: Optional[Usuario] = Relationship(back_populates="movimientos")