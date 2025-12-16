from src.config.conexion_db import ConexionBD
from src.view.inventario.frm_nuevo_libro import FrmNuevoLibro
from src.model.Editorial import Editorial
from src.model.Autor import Autor
from src.model.Obra import Obra
from src.model.Ejemplar import Ejemplar

class CatalogoController:
    def __init__(self, view_container, id_usuario_actual, on_close=None):
        self.view_container = view_container
        self.id_usuario_actual = id_usuario_actual
        self.on_close = on_close
        self.view = FrmNuevoLibro(view_container, self)
        # Instanciamos la conexión una sola vez
        self.db = ConexionBD()

    def volver_al_menu(self):
        if self.on_close:
            self.on_close()

    def registrar_libro_completo(self, datos):
        # 1. Validaciones OBLIGATORIAS (Lo que NO puede ser N/A)
        if not datos.get("titulo") or str(datos.get("titulo")).strip() == "":
            self.view.mostrar_mensaje("Error: El Título es obligatorio.", True)
            return

        # =========================================================================
        # ✨ MAGIA DE LIMPIEZA: Rellenar campos vacíos con "N/A"
        # =========================================================================
        # Recorremos todos los datos recibidos
        for clave, valor in datos.items():
            # Si el valor es None o está vacío (sin contar espacios)
            if valor is None or str(valor).strip() == "":
                # Excepción: No queremos poner "N/A" en campos numéricos estrictos si la BD es INT
                # Pero asumiremos que tu BD acepta texto en la mayoría (Varchar).
                datos[clave] = "N/A"
        # =========================================================================

        # Usamos el Context Manager (with)
        with self.db as conn:
            if not conn:
                self.view.mostrar_mensaje("Error de conexión a la BD", True)
                return
            
            cursor = conn.cursor()
            try:
                # Iniciamos transacción
                conn.begin() 

                # --- PASO 1: Editorial ---
                # Usamos los datos ya limpios (si venía vacío, ahora dice "N/A")
                editorial = Editorial(datos.get("editorial_nombre"), datos.get("lugar_publicacion"))
                id_editorial = editorial.guardar(cursor) 

                # --- PASO 2: Obra ---
                obra = Obra(
                    titulo=datos["titulo"],
                    id_editorial=id_editorial,
                    isbn=datos.get("isbn"),
                    idioma=datos.get("idioma"),
                    anio_publicacion=datos.get("anio"),
                    edicion=datos.get("edicion"),
                    clasificacion=datos.get("clasificacion"),
                    paginas=datos.get("paginas"),
                    dimensiones=datos.get("dimensiones"),
                    serie=datos.get("serie"),
                    tomo=datos.get("tomo"),
                    volumen=datos.get("volumen"),
                    descripcion=datos.get("descripcion"),
                    ficha_no=datos.get("ficha_no"),
                    autor_corporativo=datos.get("autor_corporativo"),
                    asientos_secundarios=datos.get("asientos_secundarios"),
                    codigo_ilustracion=datos.get("codigo_ilustracion"),
                    lugar_publicacion=datos.get("lugar_publicacion")
                )
                id_obra = obra.guardar(cursor)

                # --- PASO 3: Autor ---
                autor = Autor(datos.get("autor_nombre"))
                id_autor = autor.guardar(cursor)
                
                obra.relacionar_autor(cursor, id_autor)

                # --- PASO 4: Ejemplar ---
                ejemplar = Ejemplar(
                    id_obra=id_obra,
                    numero_copia=datos.get("numero_copia"),
                    ubicacion_fisica=datos.get("ubicacion")
                )
                id_generado = ejemplar.guardar(cursor)

                # Si todo sale bien:
                conn.commit()
                self.view.confirmar_registro(id_generado)

            except Exception as e:
                conn.rollback()
                print(f"Error CRÍTICO al guardar libro: {e}")
                self.view.mostrar_mensaje(f"Error al guardar: {e}", True)
            finally:
                cursor.close()

    def obtener_info_ejemplar(self, id_ejemplar):
        return Ejemplar.obtener_info(id_ejemplar)

    def procesar_baja(self, id_ejemplar):
        exito, msg = Ejemplar.dar_de_baja(id_ejemplar)
        return exito, msg