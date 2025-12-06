import os
import sys
import customtkinter as ctk
from src.model.Estadisticas import Estadisticas

class FrmMenuPrincipal(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        # Obtener el rol de forma segura
        rol_usuario = self.controller.app.usuario_actual.rol if self.controller and self.controller.app.usuario_actual else "Invitado"

        # Colores y grid
        self.COLOR_FONDO_MENU = "#A7744A"
        self.COLOR_FONDO_MAIN = "#F3E7D2"
        self.COLOR_BOTON_MENU = "#8c5e3c"
        self.COLOR_TEXTO = "#5a3b2e"
        
        self.configure(fg_color=self.COLOR_FONDO_MAIN)
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- BARRA LATERAL (SIDEBAR) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.COLOR_FONDO_MENU)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1) # Empujar contenido hacia arriba
        
        # LOGO
        self.lbl_logo = ctk.CTkLabel(self.sidebar_frame, text="BIBLIOTECA\nCONGRESO", font=("Georgia", 20, "bold"), text_color="white")
        self.lbl_logo.pack(pady=(30, 20), padx=20)

        # BOTONES DEL MENÚ
        self.crear_boton_menu("🔎 Consultar Libro", self.controller.mostrar_busqueda)
        self.crear_boton_menu("➕ Agregar Libro", self.controller.mostrar_catalogo)
        self.crear_boton_menu("🗑️Quitar Libro", self.controller.mostrar_baja_libros)
        self.crear_boton_menu("📑 Préstamos", self.controller.mostrar_prestamos)
        self.crear_boton_menu("👥 Lectores", self.controller.mostrar_solicitantes)
        self.crear_boton_menu("📊 Reportes", self.controller.mostrar_reportes_avanzados)
        self.crear_boton_menu("🚶 Registro Visitas", self.controller.mostrar_registro_visitas)

        # OPCIONES DE ADMIN
        if rol_usuario == "Admin":
            # Aquí está el cambio solicitado: Apartado de Configuración
            self.crear_boton_menu("⚙️ Configuración", self.controller.mostrar_usuarios_sistema) 

        #BOTÓN DE AVISO DE PRIVACIDAD
        self.btn_privacidad = ctk.CTkButton(
            self.sidebar_frame,
            text="❓",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="transparent",
            hover_color=self.COLOR_BOTON_MENU,
            font=("Arial", 24),
            command=self.abrir_privacidad
        )
        self.btn_privacidad.pack(side="bottom", anchor="sw", padx=20, pady=20)

        # --- ÁREA PRINCIPAL Y HEADER ---
        self.main_content = ctk.CTkFrame(self, fg_color=self.COLOR_FONDO_MAIN, corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.main_content.grid_rowconfigure(1, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)
        
        # Header Superior (Dentro del frame principal)
        self.header_frame = ctk.CTkFrame(self.main_content, height=60, fg_color="white", corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        self.lbl_seccion = ctk.CTkLabel(self.header_frame, text="Panel de Control", font=("Arial", 20, "bold"), text_color=self.COLOR_TEXTO)
        self.lbl_seccion.pack(side="left", padx=20, pady=10)
        
        # Botón Logout (Redundante con MenuBar pero útil visualmente)
        self.btn_logout = ctk.CTkButton(self.header_frame, text="Cerrar Sesión", fg_color="#D32F2F", hover_color="#B71C1C", width=120, height=35, command=self.controller.mostrar_login)
        self.btn_logout.pack(side="right", padx=20, pady=10)

        # --- CONTENIDO CENTRAL (Dashboard) ---
        self.dashboard_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.dashboard_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # 1. Obtenemos datos frescos (Try/Except para evitar crash si no hay DB)
        try:
            datos = Estadisticas.obtener_resumen()
        except Exception:
            datos = {"libros": 0, "prestamos": 0, "usuarios": 0}

        # 2. Creamos las tarjetas con los datos
        self.crear_tarjeta_info(self.dashboard_frame, "Obras Registradas", str(datos["libros"]), 0, 0)
        self.crear_tarjeta_info(self.dashboard_frame, "Préstamos Activos", str(datos["prestamos"]), 0, 1)
        self.crear_tarjeta_info(self.dashboard_frame, "Lectores Inscritos", str(datos["usuarios"]), 0, 2)

    # MÉTODOS AUXILIARES
    def crear_boton_menu(self, texto, comando):
        btn = ctk.CTkButton(
            self.sidebar_frame, 
            text=texto, 
            anchor="w", 
            fg_color="transparent", 
            text_color="white", 
            hover_color=self.COLOR_BOTON_MENU, 
            font=("Arial", 16, "bold"), 
            height=50, 
            command=comando
        )
        btn.pack(fill="x", padx=10, pady=5)

    def crear_tarjeta_info(self, parent, titulo, dato, fila, col):
        card = ctk.CTkFrame(parent, fg_color="white", width=250, height=150)
        card.grid(row=fila, column=col, padx=10, pady=10)
        
        # Contenedor interno para centrar
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")
        
        lbl_t = ctk.CTkLabel(inner, text=titulo, font=("Arial", 14), text_color="gray")
        lbl_t.pack()
        
        lbl_d = ctk.CTkLabel(inner, text=dato, font=("Arial", 30, "bold"), text_color=self.COLOR_TEXTO)
        lbl_d.pack()
    
     #VINCULACIÓN CON EL PDF (AVISO DE PRIVACIDAD)
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
                 print(f"No se encontró el archivo en: {ruta_completa}")