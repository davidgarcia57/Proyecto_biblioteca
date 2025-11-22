from datetime import datetime

class Prestamo:
    def __init__(self, codigo_barras, id_prestatario, id_usuario_sistema, fecha_devolucion_esperada, 
                 fecha_prestamo=None, fecha_devolucion_real=None, estado='Activo', id_prestamo=None):
        
        self.id_prestamo = id_prestamo
        
        # Relaciones (Foreign Keys)
        self.codigo_barras = codigo_barras
        self.id_prestatario = id_prestatario
        self.id_usuario_sistema = id_usuario_sistema
        
        # Fechas y Estado
        self.fecha_prestamo = fecha_prestamo if fecha_prestamo else datetime.now()
        self.fecha_devolucion_esperada = fecha_devolucion_esperada
        self.fecha_devolucion_real = fecha_devolucion_real
        self.estado = estado # 'Activo', 'Finalizado', 'Vencido'

    def __str__(self):
        return f"Prestamo {self.id_prestamo} - Libro: {self.codigo_barras}"