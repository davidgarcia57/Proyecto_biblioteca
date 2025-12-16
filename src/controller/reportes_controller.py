from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import subprocess
from datetime import datetime
from src.model.Ejemplar import Ejemplar
from src.model.Prestamo import Prestamo
from src.model.Visita import Visita

class ReportesController:
    
    def _encabezado(self, c):
        """
        Método privado para dibujar el logo y encabezado institucional.
        Se usa rutas dinámicas para que funcione en cualquier computadora.
        """
        # 1. Construimos la ruta segura:  controlador -> src -> raiz -> resources
        # __file__ es este archivo. Hacemos dirname 3 veces para subir 3 carpetas.
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ruta_logo = os.path.join(base_dir, "resources", "logo.png")

        try:
            # Dibujamos el logo en la esquina superior izquierda
            # Coordenadas (x, y, ancho, alto)
            c.drawImage(ruta_logo, 40, 730, width=60, height=60, mask='auto') 
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
        
        # Opcional: Agregar nombre de la institución como texto fijo si gustas
        c.setFont("Helvetica-Bold", 10)
        c.drawString(110, 770, "H. CONGRESO DEL ESTADO DE DURANGO")
        c.setFont("Helvetica", 9)
        c.drawString(110, 758, "Sistema de Gestión Bibliotecaria")

    def generar_reporte_visitas_areas(self, f_ini, f_fin, ruta_archivo):
        datos = Visita.obtener_conteo_por_area(f_ini, f_fin)
        
        c = canvas.Canvas(ruta_archivo, pagesize=letter)
        
        # --- AQUÍ LLAMAMOS AL LOGO ---
        self._encabezado(c) 
        # -----------------------------

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 700, "Estadística de Visitas por Área") # Bajé un poco Y por el logo
        c.setFont("Helvetica", 12)
        c.drawString(50, 680, f"Periodo: {f_ini} al {f_fin}")
        
        y = 640
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y, "ÁREA")
        c.drawString(300, y, "CANTIDAD DE VISITAS")
        c.line(100, y-5, 450, y-5)
        y -= 25
        
        total_global = 0
        c.setFont("Helvetica", 12)
        for area, cantidad in datos:
            c.drawString(100, y, area)
            c.drawString(300, y, str(cantidad))
            total_global += cantidad
            y -= 20
            
        c.line(100, y+5, 450, y+5)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y-10, "TOTAL GENERAL")
        c.drawString(300, y-10, str(total_global))
        
        c.save()
        self._abrir_pdf(ruta_archivo)

    def generar_reporte_visitas_total(self, f_ini, f_fin, ruta_archivo):
        total = Visita.obtener_conteo_total(f_ini, f_fin)
        
        c = canvas.Canvas(ruta_archivo, pagesize=letter)
        self._encabezado(c) # <--- Logo
        
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, 680, "Informe General de Afluencia")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 650, f"Desde: {f_ini}")
        c.drawString(50, 630, f"Hasta: {f_fin}")
        
        # Cuadro grande con el total
        c.rect(200, 450, 200, 100)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(300, 520, "TOTAL DE VISITANTES")
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(300, 480, str(total))
        
        c.save()
        self._abrir_pdf(ruta_archivo)

    # 1. REPORTE DE LIBROS (Con columnas nuevas: Adq, Titulo, Autor, Clasif, Fecha)
    def generar_reporte_registros(self, mes_ini, anio_ini, mes_fin, anio_fin, ruta_archivo):
        f_inicio = f"{anio_ini}-{mes_ini}-01"
        f_fin = f"{anio_fin}-{mes_fin}-28" # Ajuste simple de fin de mes
        
        datos = Ejemplar.obtener_por_fecha(f_inicio, f_fin)
        
        c = canvas.Canvas(ruta_archivo, pagesize=letter)
        self._encabezado(c)
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, 700, f"Reporte de Adquisición de Libros")
        c.setFont("Helvetica", 10)
        c.drawString(30, 685, f"Periodo: {mes_ini}/{anio_ini} al {mes_fin}/{anio_fin} | Total: {len(datos)}")
        
        # --- ENCABEZADOS NUEVOS ---
        y = 660
        c.setFont("Helvetica-Bold", 8)
        c.drawString(30, y, "ADQUISICIÓN") # numero_copia
        c.drawString(100, y, "TÍTULO")
        c.drawString(280, y, "AUTOR")
        c.drawString(400, y, "CLASIFICACIÓN")
        c.drawString(490, y, "FECHA")
        c.line(30, y-5, 580, y-5)
        y -= 15
        
        c.setFont("Helvetica", 8)
        for row in datos: 
            if y < 50: 
                c.showPage(); self._encabezado(c); y = 700; c.setFont("Helvetica", 8)

            # Recorte de textos largos para que no se encimen
            titulo = (row[1][:35] + '..') if len(row[1]) > 35 else row[1]
            autor = (row[2][:20] + '..') if row[2] and len(row[2]) > 20 else (row[2] if row[2] else "S/A")
            
            c.drawString(30, y, str(row[0])) # Adquisición
            c.drawString(100, y, titulo)
            c.drawString(280, y, autor)
            c.drawString(400, y, str(row[3])) # Clasificación
            c.drawString(490, y, str(row[4].strftime("%d/%m/%Y"))) # Fecha corta
            y -= 12
            
        c.save()
        self._abrir_pdf(ruta_archivo)

    # 2. REPORTE DE PRÉSTAMOS (Columnas: Libro, Solicitante, Tel, Fecha, Estado)
    def generar_reporte_prestamos(self, mes_ini, anio_ini, mes_fin, anio_fin, ruta_archivo):
        f_inicio = f"{anio_ini}-{mes_ini}-01"
        f_fin = f"{anio_fin}-{mes_fin}-31" 
        
        datos = Prestamo.obtener_historial_por_fecha(f_inicio, f_fin)
        
        c = canvas.Canvas(ruta_archivo, pagesize=letter)
        self._encabezado(c)
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, 700, "Reporte Histórico de Préstamos")
        c.setFont("Helvetica", 10)
        c.drawString(30, 685, f"Periodo: {mes_ini}/{anio_ini} al {mes_fin}/{anio_fin}")
        
        y = 660
        c.setFont("Helvetica-Bold", 8)
        c.drawString(30, y, "LIBRO")
        c.drawString(200, y, "SOLICITANTE")
        c.drawString(350, y, "TELÉFONO")
        c.drawString(430, y, "FECHA PRÉST.")
        c.drawString(500, y, "ESTADO")
        c.line(30, y-5, 580, y-5)
        y -= 15
        
        c.setFont("Helvetica", 8)
        for row in datos: 
            if y < 50: 
                c.showPage(); self._encabezado(c); y = 700; c.setFont("Helvetica", 8)

            titulo = (row[1][:30] + '..') if len(row[1]) > 30 else row[1]
            nombre = (row[2][:25] + '..') if len(row[2]) > 25 else row[2]

            c.drawString(30, y, titulo)
            c.drawString(200, y, nombre)
            c.drawString(350, y, str(row[3]))
            c.drawString(430, y, str(row[4].strftime("%d/%m/%Y")))
            c.drawString(500, y, str(row[5]))
            y -= 12
        
        c.save()
        self._abrir_pdf(ruta_archivo)

    # 3. NUEVO REPORTE DE SOLICITANTES
    def generar_reporte_solicitantes(self, ruta_archivo):
        from src.model.Solicitantes import Solicitante # Import local
        datos = Solicitante.obtener_todos_reporte()
        
        c = canvas.Canvas(ruta_archivo, pagesize=letter)
        self._encabezado(c)
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, 700, "Directorio de Lectores Registrados")
        
        y = 660
        c.setFont("Helvetica-Bold", 8)
        c.drawString(30, y, "ID")
        c.drawString(70, y, "NOMBRE COMPLETO")
        c.drawString(250, y, "TELÉFONO")
        c.drawString(330, y, "EMAIL")
        c.line(30, y-5, 580, y-5)
        y -= 15
        
        c.setFont("Helvetica", 8)
        for row in datos:
            if y < 50: c.showPage(); self._encabezado(c); y = 700; c.setFont("Helvetica", 8)
            
            c.drawString(30, y, str(row[0]))
            c.drawString(70, y, str(row[1])[:35])
            c.drawString(250, y, str(row[2]))
            c.drawString(330, y, str(row[3])[:40])
            y -= 12
            
        c.save()
        self._abrir_pdf(ruta_archivo)
    
    def generar_reporte_bajas(self, ruta_archivo):
        datos = Ejemplar.obtener_libros_baja()
        total = len(datos)
        
        c = canvas.Canvas(ruta_archivo, pagesize=letter)
        self._encabezado(c) # <--- Logo
        
        # Configuración de tamaño de letra
        tamano_titulo = 18 
        tamano_subtitulo = 14
        tamano_encabezado = 12
        tamano_texto = 11
        
        c.setFont("Helvetica-Bold", tamano_titulo)
        c.drawString(50, 700, "Reporte de Libros Dados de BAJA")
        
        c.setFont("Helvetica", tamano_subtitulo)
        c.drawString(50, 675, f"Total de libros descartados: {total}")
        
        y = 640
        c.setFont("Helvetica-Bold", tamano_encabezado)
        c.drawString(50, y, "ID")
        c.drawString(120, y, "TÍTULO DEL LIBRO")
        c.drawString(450, y, "UBICACIÓN / NOTA")
        
        c.line(50, y-5, 550, y-5)
        y -= 25
        
        c.setFont("Helvetica", tamano_texto)
        
        for row in datos: 
            if y < 50: 
                c.showPage()
                self._encabezado(c)
                y = 700
                c.setFont("Helvetica", tamano_texto)

            c.drawString(50, y, str(row[0]))
            c.drawString(120, y, str(row[1])[:60])
            c.drawString(450, y, str(row[3]))
            y -= 20 
            
        c.save()
        self._abrir_pdf(ruta_archivo)

    def _abrir_pdf(self, filename):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(filename)
            else:  # macOS / Linux
                subprocess.call(['open', filename] if os.name == 'posix' else ['xdg-open', filename])
        except Exception as e:
            print(f"Error al abrir PDF: {e}")