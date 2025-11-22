import customtkinter as ctk

class FrmNuevoLibro(ctk.CTkScrollableFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # --- ESTÉTICA GENERAL ---
        self.COLOR_FONDO = "#F3E7D2"      # Beige
        self.COLOR_TEXTO = "#5a3b2e"      # Marrón Oscuro
        self.COLOR_BOTON = "#A7744A"      # Bronce
        self.COLOR_HOVER = "#8c5e3c"      # Bronce Oscuro
        
        # Aplicar color de fondo al frame scrolleable
        self.configure(fg_color=self.COLOR_FONDO) 
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # --- TÍTULO PRINCIPAL ---
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text="Registro Completo de Libros", 
            font=("Georgia", 26, "bold"), 
            text_color=self.COLOR_TEXTO
        )
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(20, 30))

        # ===================================================
        # SECCIÓN 1
        # ===================================================
        self.crear_seccion("1. Datos de la Obra", 1)

        self.entry_titulo = self.crear_input("Título de la Obra *", 2, 0, 2) 
        self.entry_isbn = self.crear_input("ISBN (020)", 4, 0)
        self.entry_clasif = self.crear_input("Clasificación (050)", 4, 1)
        self.entry_serie = self.crear_input("Serie (440)", 6, 0)
        self.entry_idioma = self.crear_input("Idioma (Default: SPA)", 6, 1)
        self.entry_idioma.insert(0, "SPA")

        # Ilustración (Estilizado)
        self.lbl_ilustracion = ctk.CTkLabel(self, text="Tipo de Ilustración", font=("Georgia", 12, "bold"), text_color=self.COLOR_TEXTO)
        self.lbl_ilustracion.grid(row=8, column=0, padx=20, pady=(5, 0), sticky="w")
        
        self.cbo_ilustracion = ctk.CTkComboBox(
            self, 
            values=["X - Sin ilustraciones", "A - Ilustraciones", "B - Mapas", "D - Fotografías", "Z - Otros"],
            fg_color="white", 
            text_color="black",
            border_color=self.COLOR_BOTON,
            dropdown_fg_color="white",
            dropdown_text_color="black"
        )
        self.cbo_ilustracion.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.entry_notas = self.crear_input("Notas Generales", 8, 1) 

        # ===================================================
        # SECCIÓN 2
        # ===================================================
        self.crear_seccion("2. Autoría y Editorial", 10)
        self.entry_autor = self.crear_input("Nombre del Autor Principal *", 11, 0, 2)
        self.entry_editorial = self.crear_input("Nombre de la Editorial", 13, 0)
        self.entry_lugar = self.crear_input("Lugar de Publicación", 13, 1)

        # ===================================================
        # SECCIÓN 3
        # ===================================================
        self.crear_seccion("3. Detalles de Edición", 15)
        self.entry_edicion = self.crear_input("Edición (Ej. 2da ed.)", 16, 0)
        self.entry_anio = self.crear_input("Año de Publicación", 16, 1)
        self.entry_paginas = self.crear_input("Páginas / Volúmenes", 18, 0)
        self.entry_dimensiones = self.crear_input("Dimensiones (cm)", 18, 1)

        # ===================================================
        # SECCIÓN 4
        # ===================================================
        self.crear_seccion("4. Datos del Ejemplar Físico", 20)
        self.entry_adquisicion = self.crear_input("No. Adquisición (Etiqueta) *", 21, 0, 2)
        self.entry_ejemplar = self.crear_input("Ejemplar (Ej. Copia 1)", 23, 0)
        self.entry_tomo = self.crear_input("Tomo", 23, 1)
        self.entry_volumen = self.crear_input("Volumen", 25, 0)

        # ===================================================
        # BOTÓN
        # ===================================================
        self.btn_guardar = ctk.CTkButton(
            self, 
            text="GUARDAR REGISTRO", 
            height=45, 
            font=("Georgia", 16, "bold"), 
            fg_color=self.COLOR_BOTON, 
            hover_color=self.COLOR_HOVER,
            corner_radius=10,
            command=self.evento_guardar
        )
        self.btn_guardar.grid(row=27, column=0, columnspan=2, pady=40, padx=40, sticky="ew")

        self.lbl_mensaje = ctk.CTkLabel(self, text="", font=("Arial", 12, "bold"))
        self.lbl_mensaje.grid(row=28, column=0, columnspan=2, pady=10)

    def crear_seccion(self, texto, fila):
        # Separador Visual
        separator = ctk.CTkFrame(self, height=2, fg_color=self.COLOR_BOTON)
        separator.grid(row=fila, column=0, columnspan=2, sticky="ew", padx=20, pady=(30, 0))
        
        lbl = ctk.CTkLabel(self, text=texto, font=("Georgia", 18, "bold"), text_color=self.COLOR_TEXTO)
        lbl.grid(row=fila, column=0, columnspan=2, pady=(5, 15), sticky="w", padx=20)

    def crear_input(self, placeholder, fila, columna, colspan=1):
        lbl = ctk.CTkLabel(self, text=placeholder, font=("Georgia", 12, "bold"), text_color=self.COLOR_TEXTO)
        lbl.grid(row=fila, column=columna, padx=20, pady=(5, 0), sticky="w")
        
        entry = ctk.CTkEntry(
            self, 
            placeholder_text=placeholder,
            fg_color="white",
            text_color="black",
            border_color=self.COLOR_BOTON,
            height=35
        )
        entry.grid(row=fila+1, column=columna, columnspan=colspan, padx=20, pady=(0, 10), sticky="ew")
        return entry

    def evento_guardar(self):
        datos = {
            "titulo": self.entry_titulo.get(),
            "isbn": self.entry_isbn.get(),
            "clasificacion": self.entry_clasif.get(),
            "serie": self.entry_serie.get(),
            "idioma": self.entry_idioma.get(),
            "descripcion": self.entry_notas.get(),
            "autor_nombre": self.entry_autor.get(),
            "editorial_nombre": self.entry_editorial.get(),
            "lugar_publicacion": self.entry_lugar.get(),
            "edicion": self.entry_edicion.get(),
            "anio": self.entry_anio.get(),
            "paginas": self.entry_paginas.get(),
            "dimensiones": self.entry_dimensiones.get(),
            "codigo_barras": self.entry_adquisicion.get(), 
            "ubicacion": self.entry_ejemplar.get(), 
            
            # Campo por si me falto agregar algo ajaja
            "temas": "" 
        }
        self.controller.registrar_libro_completo(datos)
    
    def mostrar_mensaje(self, mensaje, es_error=False):
        color = "red" if es_error else "#2E7D32" # Verde oscuro para más placer
        self.lbl_mensaje.configure(text=mensaje, text_color=color)