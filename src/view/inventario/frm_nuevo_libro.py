import customtkinter as ctk
from tkinter import messagebox

class FrmNuevoLibro(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # --- PALETA DE COLORES  ---
        self.COLOR_FONDO = "#F3E7D2"      # Beige
        self.COLOR_TEXTO = "#5a3b2e"      # Marrón Oscuro
        self.COLOR_BOTON = "#A7744A"      # Bronce
        self.COLOR_HOVER = "#8c5e3c"      # Bronce Oscuro
        self.COLOR_LINEA = "#A7744A"      # Color para las líneas separadoras
        
        # Configurar fondo principal
        self.configure(fg_color=self.COLOR_FONDO)

        # --- VARIABLES DE NAVEGACIÓN ---
        self.current_step = 0
        self.steps = [] 

        # --- HEADER (Título fijo) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=40, pady=(20, 10))
        
        self.lbl_titulo_main = ctk.CTkLabel(
            self.header_frame, 
            text="Registro Completo de Libros", 
            font=("Georgia", 26, "bold"), 
            text_color=self.COLOR_TEXTO
        )
        self.lbl_titulo_main.pack(side="left")

        self.lbl_paginacion = ctk.CTkLabel(
            self.header_frame, 
            text="Paso 1 de 4", 
            font=("Arial", 14, "bold"), 
            text_color=self.COLOR_BOTON
        )
        self.lbl_paginacion.pack(side="right", anchor="s")

        # --- CONTENEDOR DE LOS PASOS ---
        # Importante: fg_color="transparent" para respetar tu fondo beige
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=10)

        # Crear los frames de cada paso
        self.crear_paso_1()
        self.crear_paso_2()
        self.crear_paso_3()
        self.crear_paso_4()

        self.steps = [self.frm_step1, self.frm_step2, self.frm_step3, self.frm_step4]

        # --- FOOTER (Botones) ---
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        self.footer_frame.pack(fill="x", side="bottom", padx=40, pady=30)

        self.btn_atras = ctk.CTkButton(
            self.footer_frame, 
            text="Atrás", 
            font=("Georgia", 14),
            fg_color="gray",
            hover_color="#666666",
            width=120,
            height=40,
            command=self.anterior_paso,
            state="disabled"
        )
        self.btn_atras.pack(side="left")

        self.btn_siguiente = ctk.CTkButton(
            self.footer_frame, 
            text="Siguiente", 
            font=("Georgia", 14, "bold"),
            fg_color=self.COLOR_BOTON,
            hover_color=self.COLOR_HOVER,
            width=150,
            height=40,
            command=self.siguiente_paso
        )
        self.btn_siguiente.pack(side="right")
        
        self.lbl_mensaje = ctk.CTkLabel(self.footer_frame, text="", font=("Arial", 12, "bold"))
        self.lbl_mensaje.place(relx=0.5, rely=0.5, anchor="center")

        # Iniciar en el paso 1
        self.mostrar_paso(0)

    # ==========================================
    #             LÓGICA VISUAL
    # ==========================================
    def crear_encabezado_paso(self, parent, texto):
        """Crea el título con la línea divisoria abajo, estilo original"""
        frame_titulo = ctk.CTkFrame(parent, fg_color="transparent")
        frame_titulo.pack(fill="x", pady=(0, 20))

        lbl = ctk.CTkLabel(
            frame_titulo, 
            text=texto, 
            font=("Georgia", 20, "bold"), 
            text_color=self.COLOR_TEXTO
        )
        lbl.pack(side="left", anchor="w")

        # Línea separadora
        linea = ctk.CTkFrame(parent, height=2, fg_color=self.COLOR_LINEA)
        linea.pack(fill="x", pady=(0, 20))

    def crear_input(self, parent, label_text, row, col, colspan=1):
        """Crea label e input idénticos a tu diseño original"""
        # Label
        lbl = ctk.CTkLabel(
            parent, 
            text=label_text, 
            font=("Georgia", 12, "bold"), 
            text_color=self.COLOR_TEXTO # Color café
        )
        lbl.grid(row=row, column=col, sticky="w", pady=(10, 5), padx=10)
        
        # Input (Blanco con borde café)
        entry = ctk.CTkEntry(
            parent, 
            placeholder_text=label_text,
            fg_color="white", 
            text_color="black",
            border_color=self.COLOR_BOTON,
            height=35
        )
        entry.grid(row=row+1, column=col, columnspan=colspan, sticky="ew", pady=(0, 5), padx=10)
        return entry

    # ==========================================
    # DEFINICIÓN DE PASOS
    # ==========================================

    def crear_paso_1(self):
        self.frm_step1 = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frm_step1.columnconfigure((0, 1), weight=1) # Grid de 2 columnas
        
        self.crear_encabezado_paso(self.frm_step1, "1. Datos de la Obra")
        
        # Frame interno para el grid, para que no choque con el encabezado pack
        grid_frame = ctk.CTkFrame(self.frm_step1, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.columnconfigure((0, 1), weight=1)

        self.entry_titulo = self.crear_input(grid_frame, "Título de la Obra *", 0, 0, colspan=2)
        self.entry_isbn = self.crear_input(grid_frame, "ISBN (020)", 2, 0)
        self.entry_clasif = self.crear_input(grid_frame, "Clasificación (050)", 2, 1)
        self.entry_serie = self.crear_input(grid_frame, "Serie (440)", 4, 0)
        
        # Idioma
        self.entry_idioma = self.crear_input(grid_frame, "Idioma (Default: SPA)", 4, 1)
        self.entry_idioma.insert(0, "SPA")
        
        self.entry_temas = self.crear_input(grid_frame, "Temas / Palabras Clave", 6, 0, colspan=2)
        self.entry_descripcion = self.crear_input(grid_frame, "Notas Generales", 8, 0, colspan=2)


    def crear_paso_2(self):
        self.frm_step2 = ctk.CTkFrame(self.container, fg_color="transparent")
        
        self.crear_encabezado_paso(self.frm_step2, "2. Autoría y Editorial")

        grid_frame = ctk.CTkFrame(self.frm_step2, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.columnconfigure((0, 1), weight=1)

        self.entry_autor = self.crear_input(grid_frame, "Nombre del Autor Principal *", 0, 0, colspan=2)
        self.entry_editorial = self.crear_input(grid_frame, "Nombre de la Editorial", 2, 0)
        self.entry_lugar = self.crear_input(grid_frame, "Lugar de Publicación", 2, 1)
        self.entry_anio = self.crear_input(grid_frame, "Año de Publicación", 4, 0)


    def crear_paso_3(self):
        self.frm_step3 = ctk.CTkFrame(self.container, fg_color="transparent")
        
        self.crear_encabezado_paso(self.frm_step3, "3. Detalles de Edición")

        grid_frame = ctk.CTkFrame(self.frm_step3, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.columnconfigure((0, 1), weight=1)

        self.entry_edicion = self.crear_input(grid_frame, "Edición (Ej. 2da ed.)", 0, 0)
        self.entry_paginas = self.crear_input(grid_frame, "Páginas", 0, 1)
        self.entry_dimensiones = self.crear_input(grid_frame, "Dimensiones (cm)", 2, 0)
        
        # Nuevos campos
        self.entry_tomo = self.crear_input(grid_frame, "Tomo", 2, 1)
        self.entry_volumen = self.crear_input(grid_frame, "Volumen", 4, 0)


    def crear_paso_4(self):
        self.frm_step4 = ctk.CTkFrame(self.container, fg_color="transparent")
        
        self.crear_encabezado_paso(self.frm_step4, "4. Datos del Ejemplar Físico")

        grid_frame = ctk.CTkFrame(self.frm_step4, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.columnconfigure((0, 1), weight=1)

        self.entry_adquisicion = self.crear_input(grid_frame, "No. Adquisición (Etiqueta) *", 0, 0, colspan=2)
        
        self.entry_numero_copia = self.crear_input(grid_frame, "Ejemplar (Ej. Copia 1)", 2, 0)
        self.entry_numero_copia.insert(0, "Copia 1")
        
        self.entry_ubicacion = self.crear_input(grid_frame, "Ubicación (Ej. Pasillo 3)", 2, 1)
        self.entry_ubicacion.insert(0, "General")

    # ==========================================
    # NAVEGACIÓN Y GUARDADO
    # ==========================================

    def mostrar_paso(self, index):
        # Ocultar todos
        for step in self.steps:
            step.pack_forget()
        
        # Mostrar actual
        self.steps[index].pack(fill="both", expand=True)
        self.lbl_paginacion.configure(text=f"Paso {index + 1} de {len(self.steps)}")

        # Configurar botones
        if index == 0:
            self.btn_atras.configure(state="disabled", fg_color="gray")
        else:
            self.btn_atras.configure(state="normal", fg_color=self.COLOR_HOVER)

        if index == len(self.steps) - 1:
            self.btn_siguiente.configure(text="GUARDAR REGISTRO", fg_color="#2E7D32") # Verde
        else:
            self.btn_siguiente.configure(text="Siguiente", fg_color=self.COLOR_BOTON)

    def siguiente_paso(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.mostrar_paso(self.current_step)
        else:
            self.evento_guardar()

    def anterior_paso(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.mostrar_paso(self.current_step)

    def evento_guardar(self):
        datos = {
            "titulo": self.entry_titulo.get(),
            "isbn": self.entry_isbn.get(),
            "clasificacion": self.entry_clasif.get(),
            "serie": self.entry_serie.get(),
            "idioma": self.entry_idioma.get(),
            "temas": self.entry_temas.get(),
            "descripcion": self.entry_descripcion.get(),
            "autor_nombre": self.entry_autor.get(),
            "editorial_nombre": self.entry_editorial.get(),
            "lugar_publicacion": self.entry_lugar.get(),
            "anio": self.entry_anio.get(),
            "edicion": self.entry_edicion.get(),
            "paginas": self.entry_paginas.get(),
            "dimensiones": self.entry_dimensiones.get(),
            "tomo": self.entry_tomo.get(),
            "volumen": self.entry_volumen.get(),
            "codigo_barras": self.entry_adquisicion.get(),
            "numero_copia": self.entry_numero_copia.get(),
            "ubicacion": self.entry_ubicacion.get()
        }
        self.controller.registrar_libro_completo(datos)
    
    def mostrar_mensaje(self, mensaje, es_error=False):
        color = "red" if es_error else "#2E7D32"
        self.lbl_mensaje.configure(text=mensaje, text_color=color)