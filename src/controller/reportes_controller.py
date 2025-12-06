from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import subprocess
from datetime import datetime
from src.model.Ejemplar import Ejemplar
from src.model.Prestamo import Prestamo
from src.model.Visita import Visita

class ReportesController:
    
    def generar_reporte_visitas_areas(self, f_ini, f_fin, ruta_archivo):
        datos = Visita.obtener_conteo_por_area(f_ini, f_fin)
        
        # Usamos la ruta elegida por el usuario
        c = canvas.Canvas(ruta_archivo, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "Estadística de Visitas por Área")
        c.setFont("Helvetica", 12)
        c.drawString(50, 730, f"Periodo: {f_ini} al {f_fin}")
        
        y = 680
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
        
        # Usamos la ruta elegida por el usuario
        c = canvas.Canvas(ruta_archivo, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, 750, "Informe General de Afluencia")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 700, f"Desde: {f_ini}")
        c.drawString(50, 680, f"Hasta: {f_fin}")
        
        # Dibujar un cuadro grande con el total
        c.rect(200, 500, 200, 100)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(300, 570, "TOTAL DE VISITANTES")
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(300, 530, str(total))
        
        c.save()
        self._abrir_pdf(ruta_archivo)

    def _abrir_pdf(self, filename):
        try:
            os.startfile(filename) # Windows
        except:
            pass

    def generar_reporte_registros(self, mes_ini, anio_ini, mes_fin, anio_fin, ruta_archivo):
        # Convertir inputs a fechas MySQL (YYYY-MM-DD)
        f_inicio = f"{anio_ini}-{mes_ini}-01"
        f_fin = f"{anio_fin}-{mes_fin}-28" 
        
        datos = Ejemplar.obtener_por_fecha(f_inicio, f_fin)
        
        # Usamos la ruta elegida por el usuario
        c = canvas.Canvas(ruta_archivo, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, f"Reporte de Libros Registrados")
        c.setFont("Helvetica", 12)
        c.drawString(50, 730, f"Periodo: {mes_ini}/{anio_ini} al {mes_fin}/{anio_fin} | Total: {len(datos)}")
        
        y = 700
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "ADQUISICIÓN")
        c.drawString(150, y, "TÍTULO")
        c.drawString(450, y, "FECHA")
        y -= 20
        
        c.setFont("Helvetica", 9)
        for row in datos: # (no_adq, titulo, isbn, fecha)
            if y < 50: c.showPage(); y = 750
            c.drawString(50, y, str(row[0]))
            c.drawString(150, y, str(row[1])[:50])
            c.drawString(450, y, str(row[3]))
            y -= 15
            
        c.save()
        self._abrir_pdf(ruta_archivo)

    def generar_reporte_prestamos(self, mes_ini, anio_ini, mes_fin, anio_fin, ruta_archivo):
        f_inicio = f"{anio_ini}-{mes_ini}-01"
        f_fin = f"{anio_fin}-{mes_fin}-31" 
        
        datos = Prestamo.obtener_historial_por_fecha(f_inicio, f_fin)
        
        # Usamos la ruta elegida por el usuario
        c = canvas.Canvas(ruta_archivo, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "Reporte Histórico de Préstamos")
        c.setFont("Helvetica", 12)
        c.drawString(50, 730, f"Periodo: {mes_ini}/{anio_ini} al {mes_fin}/{anio_fin} | Total: {len(datos)}")
        
        y = 700
        c.setFont("Helvetica-Bold", 9)
        c.drawString(30, y, "LIBRO")
        c.drawString(230, y, "SOLICITANTE")
        c.drawString(380, y, "TELÉFONO")
        c.drawString(460, y, "FECHA")
        c.drawString(530, y, "ESTADO")
        y -= 20
        
        c.setFont("Helvetica", 8)
        for row in datos: 
            # (id, titulo, nombre, telefono, fecha, estado)
            if y < 50: c.showPage(); y = 750
            c.drawString(30, y, str(row[1])[:35])
            c.drawString(230, y, str(row[2])[:25])
            c.drawString(380, y, str(row[3]))
            c.drawString(460, y, str(row[4].strftime("%Y-%m-%d")))
            c.drawString(530, y, str(row[5]))
            y -= 15
            
            c.save()
            self._abrir_pdf(ruta_archivo)
    
    def generar_reporte_bajas(self, ruta_archivo):
            # 1. Obtener datos del modelo
            datos = Ejemplar.obtener_libros_baja()
            total = len(datos)
            
            # 2. Crear Canvas
            c = canvas.Canvas(ruta_archivo, pagesize=letter)
            
            # --- CONFIGURACIÓN DE TAMAÑO DE LETRA (AQUÍ SE AUMENTA) ---
            tamano_titulo = 18  # Antes solía ser 16
            tamano_subtitulo = 14 # Antes solía ser 12
            tamano_encabezado = 12 # Antes solía ser 10
            tamano_texto = 11      # Antes solía ser 9 o 8
            
            # Títulos
            c.setFont("Helvetica-Bold", tamano_titulo)
            c.drawString(50, 750, "Reporte de Libros Dados de BAJA")
            
            c.setFont("Helvetica", tamano_subtitulo)
            c.drawString(50, 725, f"Total de libros descartados: {total}")
            
            # Encabezados de la tabla
            y = 690
            c.setFont("Helvetica-Bold", tamano_encabezado)
            c.drawString(50, y, "ID")
            c.drawString(120, y, "TÍTULO DEL LIBRO")
            c.drawString(450, y, "UBICACIÓN / NOTA")
            
            # Línea separadora
            c.line(50, y-5, 550, y-5)
            y -= 25
            
            # Cuerpo del reporte
            c.setFont("Helvetica", tamano_texto)
            
            for row in datos: 
                # row = (id_ejemplar, titulo, isbn, ubicacion)
                
                # Control de salto de página si se acaba el espacio
                if y < 50: 
                    c.showPage()
                    y = 750
                    c.setFont("Helvetica", tamano_texto) # Restablecer fuente en nueva hoja
    
                c.drawString(50, y, str(row[0]))
                c.drawString(120, y, str(row[1])[:60]) # Recortar título si es muy largo
                c.drawString(450, y, str(row[3]))
                y -= 20 # Espacio entre renglones (aumentar si subes mucho la letra)
                
            c.save()
            self._abrir_pdf(ruta_archivo)