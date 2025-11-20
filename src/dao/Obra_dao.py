from src.config.conexion_db import ConexionBD
from src.model.Obra import Obra
from src.model.Editorial import Editorial
from src.model.Autor import Autor

class ObraDAO:
    
    def registrar_obra_completa(self, obra: Obra, autor: Autor, editorial: Editorial):
        """
        Realiza una transacción completa:
        1. Busca/Crea Editorial -> Obtiene ID
        2. Busca/Crea Autor -> Obtiene ID
        3. Inserta Obra -> Obtiene ID
        4. Relaciona Autor-Obra
        Retorna el ID de la obra creada o None si falla.
        """
        db = ConexionBD()
        conn = db.conectar()
        
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            conn.start_transaction()

            # Editorial
            id_editorial = self._obtener_o_crear_editorial(cursor, editorial)
            obra.id_editorial = id_editorial

            # Lo aclaro por si acaso, aqui ya no hace falta nada, ya estaria todo para agregarse a la BD
            sql_obra = """
                INSERT INTO obras (
                    titulo, isbn, clasificacion_lc, id_editorial, 
                    edicion, fecha_publicacion, paginas, dimensiones, 
                    serie, codigo_ilustracion, notas_generales
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val_obra = (
                obra.titulo, obra.isbn, obra.clasificacion_lc, obra.id_editorial,
                obra.edicion, obra.fecha_publicacion, obra.paginas, obra.dimensiones,
                obra.serie, obra.codigo_ilustracion, obra.notas_generales
            )
            cursor.execute(sql_obra, val_obra)
            id_obra_creada = cursor.lastrowid

            # Aqui se maneja lo del autor
            id_autor = self._obtener_o_crear_autor(cursor, autor)
            
            # Se manda la info a la tabla
            sql_relacion = "INSERT INTO autores_obras (id_obra, id_autor, es_principal) VALUES (%s, %s, %s)"
            cursor.execute(sql_relacion, (id_obra_creada, id_autor, True))

            conn.commit()
            print(f"Obra registrada con éxito. ID: {id_obra_creada}")
            return id_obra_creada

        except Exception as e: #Por si falla
            conn.rollback() 
            print(f"Error en transacción de Obra: {e}")
            return None
        finally:
            cursor.close()
            db.cerrar()

    def _obtener_o_crear_editorial(self, cursor, editorial: Editorial):
        # Verificar si existe por nombre, esto lo tuve que agregar para evitarnos pedos xd
        sql_buscar = "SELECT id_editorial FROM editoriales WHERE nombre_editorial = %s"
        cursor.execute(sql_buscar, (editorial.nombre_editorial,))
        resultado = cursor.fetchone()

        if resultado:
            return resultado[0] # Retorna ID existente, me recomendo que pusiera esto o algo asi
        else:
            # Insertar nueva
            sql_insertar = "INSERT INTO editoriales (nombre_editorial, lugar_publicacion) VALUES (%s, %s)"
            cursor.execute(sql_insertar, (editorial.nombre_editorial, editorial.lugar_publicacion))
            return cursor.lastrowid

    def _obtener_o_crear_autor(self, cursor, autor: Autor):
        #Igual aqui se repite lo de arriba pero con el autor
        sql_buscar = "SELECT id_autor FROM autores WHERE nombre_completo = %s"
        cursor.execute(sql_buscar, (autor.nombre_completo,))
        resultado = cursor.fetchone()

        if resultado:
            return resultado[0]
        else:
            
            sql_insertar = "INSERT INTO autores (nombre_completo, tipo_autor) VALUES (%s, %s)"
            cursor.execute(sql_insertar, (autor.nombre_completo, autor.tipo_autor))
            return cursor.lastrowid