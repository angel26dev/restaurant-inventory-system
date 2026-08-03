from sqlmodel import SQLModel, Session, create_engine

# 1. Nombre y ubicación del archivo de la base de datos
sqlite_file_name = "inventario.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 2. Motor de la base de datos (Engine)
# echo=True muestra en la terminal las instrucciones SQL reales que se están ejecutando
engine = create_engine(sqlite_url, echo=True)


# 3. Función para crear todas las tablas definidas en models.py
def crear_db_y_tablas():
    import models  # Carga los modelos para que SQLModel reconozca las estructuras

    SQLModel.metadata.create_all(engine)


# 4. Función para obtener una sesión activa de trabajo con la base de datos
def obtener_sesion():
    with Session(engine) as session:
        yield session


# Código para probar la creación de la base de datos directamente
if __name__ == "__main__":
    print("Creando base de datos y tablas...")
    crear_db_y_tablas()
    print("¡Base de datos creada con éxito!")