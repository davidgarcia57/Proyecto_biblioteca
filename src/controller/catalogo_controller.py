from src.config.conexion_db import ConexionBD
from src.view.inventario.frm_nuevo_libro import FrmNuevoLibro

# Importamos los modelos
from src.model.Editorial import Editorial
from src.model.Autor import Autor
from src.model.Obra import Obra
from src.model.Ejemplar import Ejemplar

class CatalogoController:
    def __init__(self, view_container, id_usuario_actual, on_close=None):
        self.view_container = view_container
        self.id_usuario_actual = id_usuario_actual
        self.on_close = on_close
        
        # Inicializamos la vista pasándole este controlador (self)
        self.view = FrmNuevoLibro(view_container, self)
        
        # Instanciamos el manejador de BD
        self.db = ConexionBD()

    def volver_al_menu(self):
        """
        Método llamado por el botón 'Cancelar/Atrás' de la vista (en el paso 1).
        Usa la referencia a app_main para cambiar la pantalla al menú.
        """
        if self.on_close:
            self.on_close()

    def registrar_libro_completo(self, datos):
        # 1. Validaciones básicas
        if not datos.get("titulo"):
            self.view.mostrar_mensaje("Error: El Título es obligatorio.", True)
            return

        # 2. Conexión a la Base de Datos
        conn = self.db.conectar()
        
        if not conn or not conn.is_connected():
            self.view.mostrar_mensaje("Sin conexión a BD", True)
            return

        cursor = None
        try:
            cursor = conn.cursor()
            conn.start_transaction() # Inicia transacción

            # --- PASO 1: Editorial ---
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
                temas=datos.get("temas"),
                ficha_no=datos.get("ficha_no"),
                autor_corporativo=datos.get("autor_corporativo"),
                asientos_secundarios=datos.get("asientos_secundarios"),
                codigo_ilustracion=datos.get("codigo_ilustracion"),
                analizo=datos.get("analizo"),
                reviso=datos.get("reviso"),
                lugar_publicacion=datos.get("lugar_publicacion")
            )
            id_obra = obra.guardar(cursor)

            # --- PASO 3: Autor y Relación ---
            autor = Autor(datos.get("autor_nombre", "Anónimo"))
            id_autor = autor.guardar(cursor)
            
            # Relacionamos el autor con la obra
            obra.relacionar_autor(cursor, id_autor)

            # --- PASO 4: Ejemplar ---
            ejemplar = Ejemplar(
                id_obra=id_obra,
                numero_copia=datos.get("numero_copia", "Copia 1"),
                ubicacion_fisica=datos.get("ubicacion", "General")
            )
            
            # Guardamos y CAPTURAMOS el ID que la BD acaba de generar
            id_generado = ejemplar.guardar(cursor)

            # Confirmamos la transacción
            conn.commit()
            
            # --- MENSAJE FINAL CON EL NÚMERO DE ADQUISICIÓN ---
            self.view.mostrar_mensaje(f"¡Éxito! Libro registrado.\nNo. Adquisición Asignado: {id_generado}")

        except Exception as e:
            conn.rollback() # Si falla algo, deshacemos todo
            print(f"Error: {e}")
            self.view.mostrar_mensaje(f"Error al guardar: {e}", True)
        finally:
            if cursor:
                cursor.close()
            # No cerramos la conexión self.db aquí para mantenerla disponible