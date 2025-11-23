import customtkinter as ctk

class FrmMenuPrincipal(ctk.CTkFrame):
    """
    Frame del menú principal. 
    """
class FrmMenuPrincipal(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        
        # --- PALETA DE COLORES ---
        self.COLOR_FONDO = "#F3E7D2"      # Beige 
        self.COLOR_TEXTO = "#5a3b2e"      # Marrón Oscuro 
        self.COLOR_BOTON = "#A7744A"      # Bronce 
        self.COLOR_HOVER = "#8c5e3c"      # Bronce Oscuro 
        self.COLOR_UTILIDAD = self.COLOR_TEXTO # Color para Salir/Cerrar Sesión

        # Fondo principal
        self.configure(fg_color=self.COLOR_FONDO)

        # Centrar el contenido principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Fila central de botones

        # ----------------------------------------------
        # --- 1. BOTONES DE CERRAR SESIÓN Y SALIR ---
        # ----------------------------------------------
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(25, 10))
        self.header_frame.grid_columnconfigure(0, weight=0) 
        self.header_frame.grid_columnconfigure(1, weight=1) 
        self.header_frame.grid_columnconfigure(2, weight=0) 

        # Botón Cerrar Sesión
        self.btn_cerrar_sesion = ctk.CTkButton(
            self.header_frame, 
            text="Cerrar Sesión", 
            font=("Georgia", 16, "bold"), 
            fg_color="transparent", 
            text_color=self.COLOR_UTILIDAD, 
            border_color=self.COLOR_UTILIDAD, 
            border_width=2,
            hover_color=self.COLOR_HOVER, 
            width=160,
            height=45, 
            corner_radius=10, 
            command=lambda: print("Cerrar Sesión (placeholder)") 
        )
        self.btn_cerrar_sesion.grid(row=0, column=0, sticky="w", padx=10)
        
        # Contenedor para el Título y Subtítulo
        self.title_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.title_container.grid(row=0, column=1, padx=20, sticky="n")

        self.lbl_titulo = ctk.CTkLabel(
            self.title_container, 
            text="MENÚ PRINCIPAL", 
            font=("Georgia", 40, "bold"), 
            text_color=self.COLOR_TEXTO
        )
        self.lbl_titulo.pack()

        #Aquí una pequeña descripción 
        self.lbl_subtitulo = ctk.CTkLabel(
            self.title_container,
            text="Seleccione una opción para gestionar el inventario y préstamos.",
            font=("Arial", 16), 
            text_color=self.COLOR_TEXTO 
        )
        self.lbl_subtitulo.pack(pady=(5, 15))


        # Botón Salir 
        self.btn_salir = ctk.CTkButton(
            self.header_frame, 
            text="Salir", 
            font=("Georgia", 16, "bold"), 
            fg_color="transparent", 
            text_color=self.COLOR_UTILIDAD, 
            border_color=self.COLOR_UTILIDAD, 
            border_width=2,
            hover_color=self.COLOR_HOVER, 
            width=130,
            height=45, 
            corner_radius=10, 
            command=lambda: print("Salir de la Aplicación (placeholder)")
        )
        self.btn_salir.grid(row=0, column=2, sticky="e", padx=10)

        # ----------------------------------------------
        # --- 2. BOTONES PRINCIPALES ---
        # ----------------------------------------------
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=80, pady=(50, 50))
        
        self.main_container.grid_columnconfigure((0, 1), weight=1)
        self.main_container.grid_rowconfigure((0, 1), weight=1)

        # El estilo de botón para las opciones principales
        self.MAIN_BTN_CONFIG = {
            "font": ("Georgia", 24, "bold"), 
            "fg_color": self.COLOR_BOTON,
            "hover_color": self.COLOR_HOVER,
            "text_color": "white", 
            "width": 200, 
            "height": 80,  
            "corner_radius": 15, 
            "border_width": 4, 
            "border_color": self.COLOR_TEXTO, 
            "compound": "left", 
            "anchor": "center",
            "state": "normal"
        }
        
        BTN_PADX = 25
        BTN_PADY = 25
        
        # Botón 1: Préstamos
        self.btn_prestamos = ctk.CTkButton(
            self.main_container,
            text="📑 PRÉSTAMOS", 
            command=lambda: print("Navegar a Préstamos (placeholder)"),
            **self.MAIN_BTN_CONFIG
        )
        self.btn_prestamos.grid(row=0, column=0, padx=BTN_PADX, pady=BTN_PADY, sticky="nsew")

        #Botón 2: Buscar Libros
        self.btn_buscar = ctk.CTkButton(
            self.main_container,
            text="🔎 BUSCAR LIBROS",
            command=self.controller.mostrar_busqueda,
            **self.MAIN_BTN_CONFIG
        )
        self.btn_buscar.grid(row=0, column=1, padx=BTN_PADX, pady=BTN_PADY, sticky="nsew")

        # Botón 3: Agregar
        self.btn_agregar = ctk.CTkButton(
            self.main_container,
            text="➕ AGREGAR LIBROS",
            command=self.controller.mostrar_catalogo, # <--- Navega al formulario
            **self.MAIN_BTN_CONFIG
        )
        self.btn_agregar.grid(row=1, column=0, padx=25, pady=25, sticky="nsew")

        # Botón 4: Otro 
        self.btn_otro = ctk.CTkButton(
            self.main_container,
            text="⚙️ OTRAS OPCIONES",
            command=lambda: print("Navegar a Otras Opciones (placeholder)"),
            **self.MAIN_BTN_CONFIG
        )
        self.btn_otro.grid(row=1, column=1, padx=BTN_PADX, pady=BTN_PADY, sticky="nsew")

        # Botón 5: Cerrar Sesión
        self.btn_cerrar_sesion = ctk.CTkButton(
            self.header_frame, 
            text="Cerrar Sesión", 
            command=self.controller.mostrar_login,  # <--- Llama a volver al login
            **self.MAIN_BTN_CONFIG
        )
        self.btn_cerrar_sesion.grid(row=0, column=0, sticky="w", padx=10)
        