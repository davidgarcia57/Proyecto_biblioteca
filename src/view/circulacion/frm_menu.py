import customtkinter as ctk

class FrmMenuPrincipal(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        
        # --- PALETA DE COLORES ---
        self.COLOR_FONDO_MENU = "#A7744A"    # El color Bronce para la barra lateral
        self.COLOR_FONDO_MAIN = "#F3E7D2"    # El Beige para el contenido
        self.COLOR_BOTON_MENU = "#8c5e3c"    # Un poco más oscuro para botones
        self.COLOR_TEXTO = "#5a3b2e"         # Marrón
        
        # Configuración del grid principal (2 columnas: Menú lateral y Contenido)
        self.configure(fg_color=self.COLOR_FONDO_MAIN)
        
        # Columna 0: Barra lateral (fija, ancho pequeño)
        # Columna 1: Contenido principal (se expande)
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ------------------------------------------------
        # 1. BARRA LATERAL (Izquierda)
        # ------------------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.COLOR_FONDO_MENU)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Empuja elementos hacia abajo si es necesario

        # Título / Logo en la barra
        self.lbl_logo = ctk.CTkLabel(
            self.sidebar_frame, 
            text="BIBLIOTECA\nCONGRESO", 
            font=("Georgia", 20, "bold"), 
            text_color="white"
        )
        self.lbl_logo.pack(pady=(30, 30), padx=20)

        # Botones de Navegación (Estilo menú)
        self.crear_boton_menu("🏠 Inicio", lambda: print("Ir a Inicio"))
        self.crear_boton_menu("🔎 Buscar Libros", self.controller.mostrar_busqueda)
        self.crear_boton_menu("➕ Nuevo Libro", self.controller.mostrar_catalogo)
        self.crear_boton_menu("📑 Préstamos", lambda: print("Ir a Prestamos"))
        self.crear_boton_menu("👥 Usuarios", lambda: print("Ir a Usuarios"))

        # ------------------------------------------------
        # 2. ÁREA PRINCIPAL (Derecha)
        # ------------------------------------------------
        self.main_content = ctk.CTkFrame(self, fg_color=self.COLOR_FONDO_MAIN, corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.main_content.grid_rowconfigure(1, weight=1) # Fila 1 se expande (contenido)
        self.main_content.grid_columnconfigure(0, weight=1)

        # --- HEADER (Barra superior) ---
        self.header_frame = ctk.CTkFrame(self.main_content, height=60, fg_color="white", corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        # Título de la sección actual
        self.lbl_seccion = ctk.CTkLabel(
            self.header_frame, 
            text="Panel de Control", 
            font=("Arial", 20, "bold"), 
            text_color=self.COLOR_TEXTO
        )
        self.lbl_seccion.pack(side="left", padx=20, pady=10)

        # BOTÓN CERRAR SESIÓN
        self.btn_logout = ctk.CTkButton(
            self.header_frame,
            text="Cerrar Sesión",
            fg_color="#D32F2F", # Rojo discreto para salir
            hover_color="#B71C1C",
            width=120,
            height=35,
            command=self.controller.mostrar_login # Vuelve al login
        )
        self.btn_logout.pack(side="right", padx=20, pady=10)

        # --- CONTENIDO CENTRAL (Dashboard) ---
        self.dashboard_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.dashboard_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Aquí podemos poner "Tarjetas" de resumen para que no se vea vacío
        self.crear_tarjeta_info(self.dashboard_frame, "Total Libros", "120", 0, 0)
        self.crear_tarjeta_info(self.dashboard_frame, "Préstamos Activos", "15", 0, 1)
        self.crear_tarjeta_info(self.dashboard_frame, "Usuarios Registrados", "45", 0, 2)

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
        
        lbl_t = ctk.CTkLabel(card, text=titulo, font=("Arial", 14), text_color="gray")
        lbl_t.place(relx=0.5, rely=0.3, anchor="center")
        
        lbl_d = ctk.CTkLabel(card, text=dato, font=("Arial", 30, "bold"), text_color=self.COLOR_TEXTO)
        lbl_d.place(relx=0.5, rely=0.6, anchor="center")
        