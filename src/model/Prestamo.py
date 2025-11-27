from datetime import datetime, timedelta

class Prestamo:
    def __init__(self, id_prestatario, id_usuario_sistema, id_ejemplar, 
                 fecha_devolucion_esperada, id_prestamo=None, fecha_prestamo=None, 
                 fecha_devolucion_real=None, estado='Activo'):
        
        self.id_prestamo = id_prestamo
        self.id_prestatario = id_prestatario
        self.id_usuario_sistema = id_usuario_sistema
        self.id_ejemplar = id_ejemplar
        self.fecha_prestamo = fecha_prestamo if fecha_prestamo else datetime.now()
        self.fecha_devolucion_esperada = fecha_devolucion_esperada
        self.fecha_devolucion_real = fecha_devolucion_real
        self.estado = estado 

    def guardar(self, conn):
        """
        Registra el préstamo y actualiza el estado del ejemplar.
        NOTA: Recibe 'conn' porque esto debe ser parte de una transacción controlada por el controller.
        """
        cursor = conn.cursor()
        
        # 1. Insertar el préstamo
        sql_prestamo = """
            INSERT INTO prestamos (id_prestatario, id_usuario_sistema, id_ejemplar, fecha_prestamo, fecha_devolucion_esperada, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        vals_prestamo = (
            self.id_prestatario, 
            self.id_usuario_sistema, 
            self.id_ejemplar, 
            self.fecha_prestamo, 
            self.fecha_devolucion_esperada, 
            self.estado
        )
        cursor.execute(sql_prestamo, vals_prestamo)
        self.id_prestamo = cursor.lastrowid
        
        # 2. Actualizar el estado del ejemplar a 'Prestado'
        sql_ejemplar = "UPDATE ejemplares SET estado = 'Prestado' WHERE id_ejemplar = %s"
        cursor.execute(sql_ejemplar, (self.id_ejemplar,))
        
        return self.id_prestamo

    @staticmethod
    def finalizar_prestamo(conn, id_prestamo, id_ejemplar):
        """ Registra la devolución y libera el libro """
        cursor = conn.cursor()
        
        # 1. Actualizar préstamo
        sql_fin = "UPDATE prestamos SET estado = 'Finalizado', fecha_devolucion_real = NOW() WHERE id_prestamo = %s"
        cursor.execute(sql_fin, (id_prestamo,))
        
        # 2. Liberar libro
        sql_lib = "UPDATE ejemplares SET estado = 'Disponible' WHERE id_ejemplar = %s"
        cursor.execute(sql_lib, (id_ejemplar,))