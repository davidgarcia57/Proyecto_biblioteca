from src.config.conexion_db import ConexionBD
from src.view.inventario.frm_nuevo_libro import FrmNuevoLibro

# Importamos los modelos (que ahora tienen el SQL)
from src.model.Editorial import Editorial
from src.model.Autor import Autor
from src.model.Obra import Obra
from src.model.Ejemplar import Ejemplar

class CatalogoController:
    def __init__(self, view_container, id_usuario_actual):
        self.view_container = view_container
        self.id_usuario_actual = id_usuario_actual
        self.view = FrmNuevoLibro(view_container, self)

    def registrar_libro_completo(self, datos):
        if not datos.get("titulo") or not datos.get("codigo_barras"):
            self.view.mostrar_mensaje("Error: Título y Código de Barras obligatorios.", True)
            return

        # 1. El Controlador maneja la conexión para asegurar la Transacción (Atomicidad)
        db = ConexionBD()
        conn = db.conectar()
        
        if not conn:
            self.view.mostrar_mensaje("Sin conexión a BD", True)
            return

        try:
            cursor = conn.cursor()
            conn.start_transaction() # Inicia transacción

            # --- PASO 1: Editorial ---
            # Instanciamos el modelo y le decimos: "Guárdate usando este cursor"
            editorial = Editorial(datos.get("editorial_nombre", "Sin Editorial"), datos.get("lugar_publicacion"))
            id_editorial = editorial.guardar(cursor)

            # --- PASO 2: Obra ---
            obra = Obra(
                titulo=datos["titulo"],
                id_editorial=id_editorial,
                isbn=datos.get("isbn"),
                idioma=datos.get("idioma", "Español"),
                anio_publicacion=datos.get("anio"),
                edicion=datos.get("edicion"),
                clasificacion=datos.get("clasificacion"),
                paginas=datos.get("paginas"),
                dimensiones=datos.get("dimensiones"),
                serie=datos.get("serie"),
                tomo=datos.get("tomo"),        # Nuevo
                volumen=datos.get("volumen"),  # Nuevo
                descripcion=datos.get("descripcion"),
                temas=datos.get("temas")
            )
            id_obra = obra.guardar(cursor)

            # --- PASO 3: Autor y Relación ---
            autor = Autor(datos.get("autor_nombre", "Anónimo"))
            id_autor = autor.guardar(cursor)
            
            obra.relacionar_autor(cursor, id_autor)

            # --- PASO 4: Ejemplar ---
            # Nota: Como en la vista no tienes un campo visual para "Ubicación Física" (Estante/Pasillo),
            # lo dejamos como "General" por defecto.
            ejemplar = Ejemplar(
                codigo_barras=datos["codigo_barras"],
                id_obra=id_obra,
                numero_copia=datos.get("numero_copia", "Copia 1"),
                ubicacion_fisica="General" 
            )

            if ejemplar.existe(cursor):
                raise Exception(f"El código de barras {ejemplar.codigo_barras} ya existe.")
            
            ejemplar.guardar(cursor)

            # --- PASO 3: Autor y Relación ---
            autor = Autor(datos.get("autor_nombre", "Anónimo"))
            id_autor = autor.guardar(cursor)
            
            # El modelo Obra sabe cómo relacionarse con un autor
            obra.relacionar_autor(cursor, id_autor)

            # --- PASO 4: Ejemplar ---
            ejemplar = Ejemplar(
                codigo_barras=datos["codigo_barras"],
                id_obra=id_obra,
                ubicacion_fisica=datos.get("ubicacion", "General")
            )

            if ejemplar.existe(cursor):
                raise Exception(f"El código de barras {ejemplar.codigo_barras} ya existe.")
            
            ejemplar.guardar(cursor)

            # Si todo salió bien, confirmamos cambios
            conn.commit()
            self.view.mostrar_mensaje(f"¡Libro '{obra.titulo}' registrado con éxito!")

        except Exception as e:
            conn.rollback() # Si algo falló, deshacemos todo
            print(f"Error: {e}")
            self.view.mostrar_mensaje(f"Error al guardar: {e}", True)
        finally:
            cursor.close()
            db.cerrar()