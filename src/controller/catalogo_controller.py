from src.config.conexion_db import ConexionBD
from src.view.inventario.frm_nuevo_libro import FrmNuevoLibro

# Importamos los modelos
from src.model.Editorial import Editorial
from src.model.Autor import Autor
from src.model.Obra import Obra
from src.model.Ejemplar import Ejemplar

class CatalogoController:
    def __init__(self, view_container, id_usuario_actual, app_main=None):
        self.view_container = view_container
        self.id_usuario_actual = id_usuario_actual
        self.app_main = app_main  # Referencia a la App principal para poder navegar
        
        # Inicializamos la vista pasándole este controlador (self)
        self.view = FrmNuevoLibro(view_container, self)
        
        # OPTIMIZACIÓN: Instanciamos el manejador de BD una sola vez al inicio
        self.db = ConexionBD()

    def volver_al_menu(self):
        """
        Método llamado por el botón 'Cancelar/Atrás' de la vista (en el paso 1).
        Usa la referencia a app_main para cambiar la pantalla al menú.
        """
        if self.app_main:
            self.app_main.mostrar_menu_principal()

    def registrar_libro_completo(self, datos):
        # Validaciones básicas antes de tocar la BD
        if not datos.get("titulo") or not datos.get("codigo_barras"):
            self.view.mostrar_mensaje("Error: Título y Código de Barras obligatorios.", True)
            return

        # 1. Intentamos conectar (o reusar la conexión si ya está abierta)
        conn = self.db.conectar()
        
        # Verificamos si realmente tenemos conexión
        if not conn or not conn.is_connected():
            self.view.mostrar_mensaje("Sin conexión a BD", True)
            return

        cursor = None
        try:
            cursor = conn.cursor()
            conn.start_transaction() # Inicia transacción (Atomicidad)

            # --- PASO 1: Editorial ---
            # Busca si existe la editorial o la crea
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
                tomo=datos.get("tomo"),
                volumen=datos.get("volumen"),
                descripcion=datos.get("descripcion"),
                temas=datos.get("temas")
            )
            id_obra = obra.guardar(cursor)

            # --- PASO 3: Autor y Relación ---
            autor = Autor(datos.get("autor_nombre", "Anónimo"))
            id_autor = autor.guardar(cursor)
            
            # Relacionamos el autor con la obra en la tabla intermedia
            obra.relacionar_autor(cursor, id_autor)

            # --- PASO 4: Ejemplar ---
            ejemplar = Ejemplar(
                codigo_barras=datos["codigo_barras"],
                id_obra=id_obra,
                numero_copia=datos.get("numero_copia", "Copia 1"),
                ubicacion_fisica=datos.get("ubicacion", "General")
            )

            # Verificamos si el código de barras ya existe para evitar duplicados
            if ejemplar.existe(cursor):
                raise Exception(f"El código de barras {ejemplar.codigo_barras} ya existe.")
            
            ejemplar.guardar(cursor)

            # Si todo salió bien, confirmamos cambios permanentemente
            conn.commit()
            self.view.mostrar_mensaje(f"¡Libro '{obra.titulo}' registrado con éxito!")

        except Exception as e:
            conn.rollback() # Si algo falló, deshacemos todo lo anterior
            print(f"Error: {e}")
            self.view.mostrar_mensaje(f"Error al guardar: {e}", True)
        finally:
            if cursor:
                cursor.close()
            # NOTA: NO cerramos 'db.cerrar()' aquí para mantener la conexión viva 
            # y que el siguiente libro se guarde más rápido.