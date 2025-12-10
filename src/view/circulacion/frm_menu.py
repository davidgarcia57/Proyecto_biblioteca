import os
import sys
import customtkinter as ctk
from tkinter import messagebox
from src.model.Estadisticas import Estadisticas
from src.utils import resource_path

class FrmMenuPrincipal(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        
        self.usuario = self.controller.app.usuario_actual
        rol_usuario = self.usuario.rol if self.usuario else "Invitado"
        nombre_usuario = self.usuario.nombre if self.usuario else "Usuario"

        # --- PALETA DE COLORES ---
        self.COLOR_FONDO_MENU = "#A7744A"
        self.COLOR_FONDO_MAIN = "#F3E7D2" 
        self.COLOR_BOTON_MENU = "#8c5e3c"
        self.COLOR_TEXTO = "#000000" # CAMBIO: Negro puro para máximo contraste
        self.COLOR_TARJETAS = "#FFFFFF"
        
        self.configure(fg_color=self.COLOR_FONDO_MAIN)
        
        # Grid: Sidebar (280px para dar más aire) y Main
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)
        
        # =================================================
        #              1. BARRA LATERAL (SIDEBAR)
        # =================================================
        # CAMBIO: Ancho aumentado de 250 a 280 para acomodar letra grande
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=self.COLOR_FONDO_MENU)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1) 
        
        # CAMBIO: Logo más grande y Arial
        self.lbl_logo = ctk.CTkLabel(
            self.sidebar_frame, 
            text="BIBLIOTECA\nCONGRESO", 
            font=("Arial", 26, "bold"), # De Georgia 22 a Arial 26
            text_color="white"
        )
        self.lbl_logo.pack(pady=(40, 40), padx=20)

        # Botones del Menú (Ver método crear_boton_menu más abajo para los cambios de tamaño)
        self.crear_boton_menu(" 🔍 Consultar Libro", self.controller.mostrar_busqueda)
        self.crear_boton_menu(" ➕ Agregar Libro", self.controller.mostrar_catalogo)
        self.crear_boton_menu(" ➖ Quitar Libro", self.controller.mostrar_baja_libros)
        
        # Separador visual más notorio
        ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="#D7CCC8").pack(fill="x", padx=20, pady=15)
        
        self.crear_boton_menu(" ⏳ Préstamos", self.controller.mostrar_prestamos)
        self.crear_boton_menu(" ✅ Devoluciones", self.controller.mostrar_lista_prestamos) 
        self.crear_boton_menu(" 👥 Lectores", self.controller.mostrar_solicitantes)
        
        self.crear_boton_menu(" 📊 Reportes", self.controller.mostrar_reportes_avanzados)
        self.crear_boton_menu(" 🚶 Visitas", self.controller.mostrar_registro_visitas)

        if rol_usuario == "Admin":
            ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="white").pack(fill="x", padx=20, pady=10)
            self.crear_boton_menu("⚙️ Config", self.controller.mostrar_usuarios_sistema)

        # Botón Privacidad
        self.btn_privacidad = ctk.CTkButton(
            self.sidebar_frame, 
            text="Aviso de Privacidad", 
            fg_color="transparent",
            hover_color=self.COLOR_BOTON_MENU, 
            font=("Arial", 16), # CAMBIO: De 12 a 16px
            height=40,          # CAMBIO: Más altura
            text_color="#E0E0E0",
            command=self.abrir_privacidad
        )
        self.btn_privacidad.pack(side="bottom", pady=20)

        # =================================================
        #              2. ÁREA PRINCIPAL
        # =================================================
        self.main_content = ctk.CTkFrame(self, fg_color=self.COLOR_FONDO_MAIN, corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.main_content.grid_rowconfigure(1, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)
        
        # --- HEADER ---
        # CAMBIO: Altura de 70 a 90 para que respire el texto grande
        self.header_frame = ctk.CTkFrame(self.main_content, height=90, fg_color="white", corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        self.lbl_seccion = ctk.CTkLabel(
            self.header_frame, 
            text=f"Bienvenido, {nombre_usuario}", 
            font=("Arial", 28, "bold"), # CAMBIO: Arial y más grande (28px)
            text_color=self.COLOR_TEXTO
        )
        self.lbl_seccion.pack(side="left", padx=30, pady=20)
        
        # CAMBIO: Botón de Salir GRANDE y ROJO
        self.btn_logout = ctk.CTkButton(
            self.header_frame, 
            text="Cerrar Sesión", 
            font=("Arial", 16, "bold"), # Letra legible
            fg_color="#D32F2F", 
            hover_color="#B71C1C", 
            width=150,  # Más ancho
            height=50,  # Más alto (fácil de clicar)
            command=self.confirmar_salida
        )
        self.btn_logout.pack(side="right", padx=30)

        # =================================================
        #              3. DASHBOARD (CENTRO)
        # =================================================
        self.dashboard_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.dashboard_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
        
        self.dashboard_frame.columnconfigure((0, 1, 2), weight=1)
        
        try:
            datos = Estadisticas.obtener_resumen()
        except Exception:
            datos = {"libros": 0, "prestamos": 0, "usuarios": 0}

        # Tarjetas de Información
        self.crear_tarjeta_info(self.dashboard_frame, "Total Obras", str(datos["libros"]), "📚", 0, 0)
        self.crear_tarjeta_info(self.dashboard_frame, "En Préstamo", str(datos["prestamos"]), "⏳", 0, 1)
        self.crear_tarjeta_info(self.dashboard_frame, "Lectores", str(datos["usuarios"]), "👥", 0, 2)

        # --- ACCESOS RÁPIDOS ---
        lbl_rapidos = ctk.CTkLabel(
            self.dashboard_frame, 
            text="Accesos Rápidos", 
            font=("Arial", 22, "bold"), # CAMBIO: Título de sección más grande
            text_color=self.COLOR_TEXTO
        )
        lbl_rapidos.grid(row=1, column=0, sticky="w", pady=(40, 15), padx=10)

        frame_acciones = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        frame_acciones.grid(row=2, column=0, columnspan=3, sticky="ew")
        
        # CAMBIO: Grid 2x2 en lugar de 1 fila de 4. 
        # En pantallas 1024px, 4 botones gigantes en fila no caben bien. 2x2 es mejor.
        frame_acciones.columnconfigure((0, 1), weight=1)
        
        # Fila 1 de botones
        self.crear_boton_rapido(frame_acciones, "Nueva Visita", "🚶", self.controller.mostrar_registro_visitas, 0, 0)
        self.crear_boton_rapido(frame_acciones, "Prestar Libro", "📖", self.controller.mostrar_prestamos, 0, 1)
        
        # Fila 2 de botones
        self.crear_boton_rapido(frame_acciones, "Devolver Libro", "✅", self.controller.mostrar_lista_prestamos, 1, 0)
        self.crear_boton_rapido(frame_acciones, "Buscar Libro", "🔍", self.controller.mostrar_busqueda, 1, 1)


    # =================================================
    #              MÉTODOS AUXILIARES
    # =================================================
    def crear_boton_menu(self, texto, comando):
        # CAMBIO: Botones del menú lateral mucho más grandes
        btn = ctk.CTkButton(
            self.sidebar_frame, 
            text=texto, 
            anchor="w", 
            fg_color="transparent", 
            text_color="white", 
            hover_color=self.COLOR_BOTON_MENU, 
            font=("Arial", 18, "bold"), # De 15 a 18px
            height=55,                  # De 45 a 55px de alto (menos probabilidad de error)
            command=comando
        )
        btn.pack(fill="x", padx=10, pady=5) # Más separación vertical (pady=5)

    def crear_tarjeta_info(self, parent, titulo, dato, icono, fila, col):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, border_color="#D7CCC8", border_width=2)
        card.grid(row=fila, column=col, padx=10, pady=10, sticky="nsew")
        
        bar = ctk.CTkFrame(card, height=15, fg_color=self.COLOR_FONDO_MENU, corner_radius=0)
        bar.pack(fill="x", side="top")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(expand=True, pady=15)
        
        # CAMBIO: Iconos y textos masivos para lectura instantánea
        ctk.CTkLabel(inner, text=icono, font=("Arial", 50)).pack(pady=(0, 5)) # Icono 50px
        ctk.CTkLabel(inner, text=dato, font=("Arial", 42, "bold"), text_color=self.COLOR_TEXTO).pack() # Dato 42px
        ctk.CTkLabel(inner, text=titulo, font=("Arial", 18), text_color="#555555").pack() # Título 18px

    def crear_boton_rapido(self, parent, texto, icono, comando, fila, col):
        # CAMBIO: Botones de acceso rápido gigantes
        btn = ctk.CTkButton(
            parent, 
            text=f"{icono}  {texto}", 
            font=("Arial", 20, "bold"), # Letra 20px
            height=80,                  # Altura 80px (Objetivo muy fácil)
            fg_color="white",
            text_color=self.COLOR_TEXTO,
            hover_color="#EBEBEB",
            border_color=self.COLOR_FONDO_MENU,
            border_width=2,
            command=comando
        )
        # Ajustamos el grid para soportar la configuración 2x2
        btn.grid(row=fila, column=col, padx=15, pady=10, sticky="ew")

    def abrir_privacidad(self):
        filename = "assets/AVISO DE PRIVACIDAD INTEGRAL DE LOS SERVICIOS BIBLIOTECARIOS.pdf"
        ruta_pdf = resource_path(filename)

        if os.path.exists(ruta_pdf):
            try:
                os.startfile(ruta_pdf)
            except Exception as e:
                messagebox.ERROR(f"Error al abrir PDF: {e}")
        else:
            messagebox.ERROR(f"No se encontró el archivo: {ruta_pdf}")

    def confirmar_salida(self):
        # CAMBIO: No podemos cambiar el tamaño de letra del messagebox nativo fácilmente,
        # pero el resto de la app ya ayuda.
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro que desea cerrar su sesión?")
        if respuesta:
            if hasattr(self.controller, 'cerrar_sesion'):
                self.controller.cerrar_sesion()
            else:
                self.controller.mostrar_login()