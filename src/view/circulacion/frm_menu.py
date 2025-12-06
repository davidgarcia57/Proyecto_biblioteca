import os
import sys
import customtkinter as ctk
from tkinter import messagebox
from src.model.Estadisticas import Estadisticas

class FrmMenuPrincipal(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        
        # Obtener datos del usuario
        self.usuario = self.controller.app.usuario_actual
        rol_usuario = self.usuario.rol if self.usuario else "Invitado"
        nombre_usuario = self.usuario.nombre if self.usuario else "Usuario"

        # --- PALETA DE COLORES ---
        self.COLOR_FONDO_MENU = "#A7744A"
        self.COLOR_FONDO_MAIN = "#F3E7D2" # Beige
        self.COLOR_BOTON_MENU = "#8c5e3c"
        self.COLOR_TEXTO = "#5a3b2e"
        self.COLOR_TARJETAS = "#FFFFFF"
        
        self.configure(fg_color=self.COLOR_FONDO_MAIN)
        self.grid_columnconfigure(0, weight=0) # Sidebar fija
        self.grid_columnconfigure(1, weight=1) # Main expandible
        self.grid_rowconfigure(0, weight=1)
        
        # =================================================
        #              1. BARRA LATERAL (SIDEBAR)
        # =================================================
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.COLOR_FONDO_MENU)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1) 
        
        self.lbl_logo = ctk.CTkLabel(self.sidebar_frame, text="BIBLIOTECA\nCONGRESO", 
                                     font=("Georgia", 22, "bold"), text_color="white")
        self.lbl_logo.pack(pady=(40, 30), padx=20)

        # Botones del Menú
        self.crear_boton_menu(" Consultar Libro", self.controller.mostrar_busqueda)
        self.crear_boton_menu(" Agregar Libro", self.controller.mostrar_catalogo)
        self.crear_boton_menu(" Quitar Libro", self.controller.mostrar_baja_libros)
        self.crear_boton_menu(" Préstamos", self.controller.mostrar_prestamos)
        self.crear_boton_menu(" Lectores", self.controller.mostrar_solicitantes)
        self.crear_boton_menu(" Reportes", self.controller.mostrar_reportes_avanzados)
        self.crear_boton_menu(" Visitas", self.controller.mostrar_registro_visitas)

        if rol_usuario == "Admin":
            ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="white").pack(fill="x", padx=20, pady=10) # Separador
            self.crear_boton_menu("⚙️ Configuración", self.controller.mostrar_usuarios_sistema)

        # Botón Privacidad (abajo)
        self.btn_privacidad = ctk.CTkButton(
            self.sidebar_frame, text="Aviso de Privacidad", fg_color="transparent",
            hover_color=self.COLOR_BOTON_MENU, font=("Arial", 12), text_color="#E0E0E0",
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
        self.header_frame = ctk.CTkFrame(self.main_content, height=70, fg_color="white", corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        # Saludo Personalizado
        self.lbl_seccion = ctk.CTkLabel(
            self.header_frame, 
            text=f"Bienvenido, {nombre_usuario}", 
            font=("Georgia", 24, "bold"), 
            text_color=self.COLOR_TEXTO
        )
        self.lbl_seccion.pack(side="left", padx=30, pady=15)
        
        self.btn_logout = ctk.CTkButton(
            self.header_frame, text="Cerrar Sesión", fg_color="#D32F2F", 
            hover_color="#B71C1C", width=120, height=35, 
            command=self.confirmar_salida
        )
        self.btn_logout.pack(side="right", padx=30)

        # =================================================
        #              3. DASHBOARD (CENTRO)
        # =================================================
        self.dashboard_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.dashboard_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        
        # Configuración de Grid del Dashboard
        self.dashboard_frame.columnconfigure((0, 1, 2), weight=1)
        
        # --- DATOS (KPIs) ---
        try:
            datos = Estadisticas.obtener_resumen()
        except Exception:
            datos = {"libros": 0, "prestamos": 0, "usuarios": 0}

        # Tarjetas de Información (Fila 0)
        self.crear_tarjeta_info(self.dashboard_frame, "Total Obras", str(datos["libros"]), "📚", 0, 0)
        self.crear_tarjeta_info(self.dashboard_frame, "Préstamos Activos", str(datos["prestamos"]), "⏳", 0, 1)
        self.crear_tarjeta_info(self.dashboard_frame, "Lectores Inscritos", str(datos["usuarios"]), "👥", 0, 2)

        # --- ACCESOS RÁPIDOS (Fila 1) ---
        # Esto rellena el espacio vacío y da utilidad
        lbl_rapidos = ctk.CTkLabel(self.dashboard_frame, text="Accesos Rápidos", 
                                   font=("Arial", 18, "bold"), text_color=self.COLOR_TEXTO)
        lbl_rapidos.grid(row=1, column=0, sticky="w", pady=(40, 10), padx=10)

        frame_acciones = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        frame_acciones.grid(row=2, column=0, columnspan=3, sticky="ew")
        frame_acciones.columnconfigure((0, 1, 2), weight=1)

        self.crear_boton_rapido(frame_acciones, "Nueva Visita", "🚶", self.controller.mostrar_registro_visitas, 0)
        self.crear_boton_rapido(frame_acciones, "Prestar Libro", "📖", self.controller.mostrar_prestamos, 1)
        self.crear_boton_rapido(frame_acciones, "Buscar Libro", "🔍", self.controller.mostrar_busqueda, 2)


    # =================================================
    #              MÉTODOS AUXILIARES
    # =================================================
    def crear_boton_menu(self, texto, comando):
        btn = ctk.CTkButton(
            self.sidebar_frame, text=texto, anchor="w", fg_color="transparent", 
            text_color="white", hover_color=self.COLOR_BOTON_MENU, 
            font=("Arial", 15, "bold"), height=45, command=comando
        )
        btn.pack(fill="x", padx=10, pady=2)

    def crear_tarjeta_info(self, parent, titulo, dato, icono, fila, col):
        # Tarjeta con borde superior de color
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, border_color="#E0E0E0", border_width=2)
        card.grid(row=fila, column=col, padx=15, pady=10, sticky="nsew")
        
        # Decoración superior (Barra de color)
        bar = ctk.CTkFrame(card, height=10, fg_color=self.COLOR_FONDO_MENU, corner_radius=0)
        bar.pack(fill="x", side="top")

        # Contenido
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(expand=True, pady=20)
        
        ctk.CTkLabel(inner, text=icono, font=("Arial", 40)).pack(pady=(0, 5))
        ctk.CTkLabel(inner, text=dato, font=("Georgia", 36, "bold"), text_color=self.COLOR_TEXTO).pack()
        ctk.CTkLabel(inner, text=titulo, font=("Arial", 14), text_color="gray").pack()

    def crear_boton_rapido(self, parent, texto, icono, comando, col):
        btn = ctk.CTkButton(
            parent, 
            text=f"{icono}  {texto}", 
            font=("Arial", 16, "bold"),
            height=60,
            fg_color="white",
            text_color=self.COLOR_TEXTO,
            hover_color="#EBEBEB",
            border_color=self.COLOR_FONDO_MENU,
            border_width=2,
            command=comando
        )
        btn.grid(row=0, column=col, padx=15, sticky="ew")

    def abrir_privacidad(self):
        filename = "AVISO DE PRIVACIDAD INTEGRAL DE LOS SERVICIOS BIBLIOTECARIOS.pdf"
        if getattr(sys,'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.getcwd() 
        ruta_completa = os.path.join(base_path,filename)
        if os.path.exists(ruta_completa):
            try:
                os.startfile(ruta_completa)
            except Exception as e:
                print(f"Error al abrir PDF: {e}")
        else:
            print(f"No se encontró el archivo: {ruta_completa}")

    def confirmar_salida(self):
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro que desea cerrar su sesión?")
        if respuesta:
            # Si dice que SÍ, llamamos al método del controlador/router
            if hasattr(self.controller, 'cerrar_sesion'):
                self.controller.cerrar_sesion()
            else:
                self.controller.mostrar_login()