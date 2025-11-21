from src.model.Obra import Obra
from src.model.Autor import Autor
from src.model.Editorial import Editorial
from src.model.Ejemplar import Ejemplar

from src.dao.Obra_dao import ObraDAO
from src.dao.Ejemplar_dao import EjemplarDAO
from src.view.inventario.frm_nuevo_libro import FrmNuevoLibro

class CatalogoController:
    def __init__(self, view_container, id_usuario_actual=1):

        self.view_container = view_container
        self.id_usuario_actual = id_usuario_actual #de momento es 1 para la DEMO
        
        # Estos son los archivos que usa que la carpeta dao
        self.obra_dao = ObraDAO()
        self.ejemplar_dao = EjemplarDAO()

        # Vista
        self.view = FrmNuevoLibro(view_container, self)

    def registrar_libro_completo(self, datos):
        """
        Recibe un diccionario 'datos' desde la Vista con TODA la información.
        Orquesta la creación de objetos y la persistencia en BD.
        """
        
        # Todo esto en si son validaciones para evitar copias y problemas en la BD
        if not datos.get("titulo") or not datos.get("no_adquisicion"):
            self.view.mostrar_mensaje("Error: Título y No. Adquisición son obligatorios.", True)
            return

        if self.ejemplar_dao.existe_adquisicion(datos["no_adquisicion"]):
            self.view.mostrar_mensaje(f"Error: El No. Adquisición {datos['no_adquisicion']} ya existe.", True)
            return

        try:
            # Es la creacion de objetos y los modelos por si acaso lo especifico pero se explican solos
            
            # Editorial
            editorial = Editorial(
                nombre_editorial=datos.get("editorial_nombre", "Sin Editorial"),
                lugar_publicacion=datos.get("lugar_publicacion")
            )

            # Autor
            autor = Autor(
                nombre_completo=datos.get("autor_nombre", "Anónimo"),
                tipo_autor="Personal" #R
            )

            # Obra
            obra = Obra(
                titulo=datos["titulo"],
                isbn=datos.get("isbn"),
                clasificacion_lc=datos.get("clasificacion"),
                edicion=datos.get("edicion"),
                fecha_publicacion=datos.get("anio"), #Por pedos de no poder usar la ñ
                paginas=datos.get("paginas"),
                dimensiones=datos.get("dimensiones"),
                serie=datos.get("serie"),
                codigo_ilustracion=datos.get("codigo_ilustracion"), # Aqui deberia ser de la A a la Z pero por practicidad solo seran unas pocas (demo)
                notas_generales=datos.get("notas"),
                codigo_idioma=datos.get("idioma", "SPA") # Lo agregue por que logicamente todos los libros estan en español pero ps si esta en otro idioma se cambia
            )

            # Es la transaccion uno (dato curioso en el extraordinario de BD fue donde la miss sin darse cuenta me estaba resolviendo todo lo que va aqui xd)
            # Esto guarda Editorial + Autor + Obra + Relaciones y devuelve el ID
            id_obra_generado = self.obra_dao.registrar_obra_completa(obra, autor, editorial)

            if not id_obra_generado:
                self.view.mostrar_mensaje("Error crítico al registrar la Obra/Autor.", True)
                return

            # CREACIÓN Y PERSISTENCIA DEL EJEMPLAR Transacción 2
            ejemplar = Ejemplar(
                no_adquisicion=datos["no_adquisicion"],
                id_obra=id_obra_generado,
                id_usuario_captura=self.id_usuario_actual,
                ejemplar=datos.get("num_ejemplar"), # Ej. "Copia 1 si llega a haber claro"
                volumen=datos.get("volumen"),
                tomo=datos.get("tomo")
            )

            exito_ejemplar = self.ejemplar_dao.guardar_ejemplar(ejemplar)

            # RESULTADO FINAL
            if exito_ejemplar:
                self.view.mostrar_mensaje(f"¡Libro '{datos['titulo']}' registrado con éxito!")
                # Opcional: Limpiar formulario
                # self.view.limpiar_campos() agrego esto o nel?
            else:
                self.view.mostrar_mensaje("La Obra se guardó, pero falló el Ejemplar físico.", True)

        except Exception as e:
            print(f"Excepción en controlador: {e}")
            self.view.mostrar_mensaje(f"Error inesperado: {e}", True)