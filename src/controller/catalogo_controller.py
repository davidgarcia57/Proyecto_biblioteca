from src.model.Libro import Libro
from src.dao.libro_dao import LibroDAO
from src.view.inventario.frm_nuevo_libro import FrmNuevoLibro

class CatalogoController:
    def __init__(self, view_container):
        # view_container será la ventana principal donde incrustaremos la vista
        self.view_container = view_container 
        self.dao = LibroDAO()
        

        self.view = FrmNuevoLibro(view_container, self)

    def registrar_libro(self, datos):
        # 1. Validar datos (Lógica de negocio)
        if not datos["titulo"] or not datos["editorial"]:
            self.view.mostrar_mensaje("El título y la editorial son obligatorios.", True)
            return

        try:
            id_editorial = int(datos["editorial"])
        except ValueError:
            self.view.mostrar_mensaje("La editorial debe ser un número.", True)
            return

        # 2. Crear objeto Modelo
        nuevo_libro = Libro(
            titulo=datos["titulo"],
            isbn=datos["isbn"],
            clasificacion=datos["clasificacion"],
            id_editorial=id_editorial
        )

        # 3. Llamar al DAO
        exito = self.dao.guardar(nuevo_libro)

        # 4. Actualizar Vista
        if exito:
            self.view.mostrar_mensaje("¡Libro registrado correctamente!")
        else:
            self.view.mostrar_mensaje("Error al guardar en base de datos.", True)