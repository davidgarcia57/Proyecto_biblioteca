import customtkinter as ctk
from tkinter import StringVar

class FmrBuscarLibro(ctk.CTkFrame):
    
    # --- PALETA DE COLORES ---
    COLOR_FONDO = "#F3E7D2"
    COLOR_TEXTO = "#5a3b2e"
    COLOR_BOTON = "#A7744A"
    COLOR_HOVER = "#8c5e3c"
    
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller 
        
        self.configure(fg_color=self.COLOR_FONDO)
        self.texto_busqueda = StringVar(value="")
        
        # Grid principal 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # El contenido se expande, el header no

        # --- HEADER CON BOTÓN VOLVER ---
        self.crear_header()
        
        # --- ÁREA DE BÚSQUEDA ---
        self.crear_elementos_busqueda()

    def crear_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        
        self.btn_volver = ctk.CTkButton(
            header_frame,
            text="⬅ Volver al Menú",
            font=("Arial", 12, "bold"),
            fg_color="transparent",
            text_color=self.COLOR_BOTON,
            border_width=2,
            border_color=self.COLOR_BOTON,
            hover_color=self.COLOR_FONDO, # Efecto sutil
            width=100,
            command=self.volver_menu
        )
        self.btn_volver.pack(side="left")

        lbl_titulo = ctk.CTkLabel(
            header_frame, 
            text="Catálogo de Libros", 
            font=("Georgia", 24, "bold"), 
            text_color=self.COLOR_TEXTO
        )
        lbl_titulo.pack(side="left", padx=20)

    def crear_elementos_busqueda(self):
        # Contenedor para centrar la búsqueda
        frame_busqueda = ctk.CTkFrame(self, fg_color="transparent")
        frame_busqueda.grid(row=1, column=0, sticky="n", pady=30)
        
        self.txt_busqueda = ctk.CTkEntry(
            frame_busqueda, 
            textvariable=self.texto_busqueda,
            placeholder_text="Título, Autor o ISBN del libro...",
            height=40,
            width=400, # Un poco más ancho
            fg_color="white", 
            text_color="black",
            border_color=self.COLOR_BOTON,
            border_width=2,
            font=("Arial", 14)
        )
        self.txt_busqueda.grid(row=0, column=0, padx=(0, 10))

        self.btn_buscar = ctk.CTkButton(
            frame_busqueda,
            text="🔍 BUSCAR",
            width=120,
            height=40,
            font=("Georgia", 14, "bold"),
            fg_color=self.COLOR_BOTON,
            hover_color=self.COLOR_HOVER,
            text_color="white",
            command=self.placeholder_funcion_buscar 
        )
        self.btn_buscar.grid(row=0, column=1)
        
    def placeholder_funcion_buscar(self):
        termino = self.texto_busqueda.get() 
        print(f"Botón Buscar presionado. Se buscaría el término: {termino}")

    def volver_menu(self):
        if self.controller:
            self.controller.mostrar_menu_principal()