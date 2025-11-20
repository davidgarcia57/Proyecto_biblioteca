import customtkinter as ctk

class FrmNuevoLibro(ctk.CTkScrollableFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller  
        
        # Es para que el grid no valga madres, todavía no lo modifico para que se vea diferente (DEMO)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Este es el TÍTULO PRINCIPAL o (Fila 0) 
        self.lbl_titulo = ctk.CTkLabel(self, text="Registro Completo de Libros", font=("Arial", 24, "bold"))
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # SECCIÓN 1: DATOS DE LA OBRA 

        # Fila 1 aqui va el título
        self.crear_seccion("1. Datos de la Obra", 1)

        # Siempre en estos seran dos, el entry y el label para que se ponga tanto detro como fuera de la caja, en este caso la fila 2 y 3
        self.entry_titulo = self.crear_input("Título de la Obra *", 2, 0, 2) 
        
<<<<<<< HEAD
        # Título
        self.lbl_titulo = ctk.CTkLabel(self, text="Ficha de Ingreso - Libros", font=("Arial", 20, "bold"))
        self.lbl_titulo.pack(pady=10)

        # Input: Título del Libro
        self.entry_titulo = ctk.CTkEntry(self, placeholder_text="Título del Libro", width=300)
        self.entry_titulo.pack(pady=5)

        # Input: ISBN
        self.entry_isbn = ctk.CTkEntry(self, placeholder_text="ISBN", width=300)
        self.entry_isbn.pack(pady=5)

        # Input: Clasificación
        self.entry_clasif = ctk.CTkEntry(self, placeholder_text="Clasificación", width=300)
        self.entry_clasif.pack(pady=5)
        
        # Input: ID Editorial (Por ahora manual, luego haremos un ComboBox)
        self.entry_editorial = ctk.CTkEntry(self, placeholder_text="ID Editorial", width=300)
        self.entry_editorial.pack(pady=5)
=======
        # Fila 4 (Labels) y 5 (Entries)
        self.entry_isbn = self.crear_input("ISBN (020)", 4, 0)
        self.entry_clasif = self.crear_input("Clasificación (050)", 4, 1)
        
        # Fila 6 (Labels) y 7 (Entries)
        self.entry_serie = self.crear_input("Serie (440)", 6, 0)
        self.entry_idioma = self.crear_input("Idioma (Default: SPA)", 6, 1)
        self.entry_idioma.insert(0, "SPA") #Esto lo agarre de un ejemplo que vi, creo que lo podemos usar para que los usuarios sepan que es cada cosa, como una guia
>>>>>>> 464ecfc27a5e9ce4ec3440ffc0d5683b428acdc7

        # Fila 8 Aquí puse lo de los codigos de ilustracion
        self.lbl_ilustracion = ctk.CTkLabel(self, text="Tipo de Ilustración")
        self.lbl_ilustracion.grid(row=8, column=0, padx=10, pady=(5, 0), sticky="w")
        
        # Fila 9 de momento no son todos los codigos pero ps es un ejemplo eda
        self.cbo_ilustracion = ctk.CTkComboBox(self, values=["X - Sin ilustraciones", "A - Ilustraciones", "B - Mapas", "D - Fotografías", "Z - Otros"])
        self.cbo_ilustracion.grid(row=9, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Fila 8 y 9 solo alinee la de notas con la de ilustraciones
        self.entry_notas = self.crear_input("Notas Generales", 8, 1) 

        # Aqui iria lo de la editorial y la autoria, más que nada me estoy basando un poco en lo que esta en la BD
        # Fila 10: Título Sección
        self.crear_seccion("2. Autoría y Editorial", 10)

        # Fila 11 (Label) y 12 (Entry)
        self.entry_autor = self.crear_input("Nombre del Autor Principal *", 11, 0, 2)
        
        # Fila 13 (Label) y 14 (Entry) Que no se note el copiar y pegar que hice en cada Label y Entry xd
        self.entry_editorial = self.crear_input("Nombre de la Editorial", 13, 0)
        self.entry_lugar = self.crear_input("Lugar de Publicación", 13, 1)

        # Ni se para que lo explico pero pos aqui va lo de detalles de la edicion como en su tabla
        # Fila 15: Título Sección
        self.crear_seccion("3. Detalles de Edición", 15)

        # Fila 16 (Label) y 17 (Entry)
        self.entry_edicion = self.crear_input("Edición (Ej. 2da ed.)", 16, 0)
        self.entry_anio = self.crear_input("Año de Publicación", 16, 1)
        
        # Fila 18 (Label) y 19 (Entry)
        self.entry_paginas = self.crear_input("Páginas / Volúmenes", 18, 0)
        self.entry_dimensiones = self.crear_input("Dimensiones (cm)", 18, 1)

        # Los datos del ejemplar fisico

        self.crear_seccion("4. Datos del Ejemplar Físico", 20)

        self.entry_adquisicion = self.crear_input("No. Adquisición (Etiqueta) *", 21, 0, 2)
        
        self.entry_ejemplar = self.crear_input("Ejemplar (Ej. Copia 1)", 23, 0)
        self.entry_tomo = self.crear_input("Tomo", 23, 1)
        
        self.entry_volumen = self.crear_input("Volumen", 25, 0)

        # Este es el boton
        # Dejamos espacio para que no choque xd 
        self.btn_guardar = ctk.CTkButton(self, text="GUARDAR REGISTRO COMPLETO", height=40, 
                                         font=("Arial", 14, "bold"), fg_color="green", hover_color="darkgreen",
                                         command=self.evento_guardar)
        self.btn_guardar.grid(row=27, column=0, columnspan=2, pady=30, padx=20, sticky="ew")

        self.lbl_mensaje = ctk.CTkLabel(self, text="")
        self.lbl_mensaje.grid(row=28, column=0, columnspan=2, pady=10)

    def crear_seccion(self, texto, fila):
        """Helper para crear separadores de sección"""
        lbl = ctk.CTkLabel(self, text=texto, font=("Arial", 16, "bold", "underline"))
        # Agregamos más pady arriba para separar secciones visualmente
        lbl.grid(row=fila, column=0, columnspan=2, pady=(25, 10), sticky="w", padx=10)

    def crear_input(self, placeholder, fila, columna, colspan=1):
        """Helper para crear entradas de texto estándar"""
        # Label en la fila 'fila'
        lbl = ctk.CTkLabel(self, text=placeholder, font=("Arial", 12))
        lbl.grid(row=fila, column=columna, padx=10, pady=(5, 0), sticky="w")
        
        # Entry en la fila 'fila + 1'
        entry = ctk.CTkEntry(self, placeholder_text=placeholder)
        entry.grid(row=fila+1, column=columna, columnspan=colspan, padx=10, pady=(0, 10), sticky="ew")
        return entry

    def evento_guardar(self):
        # Obtener la letra del código de ilustración (Ej: "A - Ilustraciones" -> "A")
        codigo_ilustracion = self.cbo_ilustracion.get().split(" - ")[0]

        # Recolectar TODOS los datos en un diccionario
        datos = {
            # Obra
            "titulo": self.entry_titulo.get(),
            "isbn": self.entry_isbn.get(),
            "clasificacion": self.entry_clasif.get(),
            "serie": self.entry_serie.get(),
            "idioma": self.entry_idioma.get(),
            "codigo_ilustracion": codigo_ilustracion,
            "notas": self.entry_notas.get(),
            
            # Autor/Editorial
            "autor_nombre": self.entry_autor.get(),
            "editorial_nombre": self.entry_editorial.get(),
            "lugar_publicacion": self.entry_lugar.get(),
            
            # Edición
            "edicion": self.entry_edicion.get(),
            "anio": self.entry_anio.get(),
            "paginas": self.entry_paginas.get(),
            "dimensiones": self.entry_dimensiones.get(),

            # Ejemplar
            "no_adquisicion": self.entry_adquisicion.get(),
            "num_ejemplar": self.entry_ejemplar.get(),
            "tomo": self.entry_tomo.get(),
            "volumen": self.entry_volumen.get()
        }
        
        # Enviar al controlador
        self.controller.registrar_libro_completo(datos)
    
    def mostrar_mensaje(self, mensaje, es_error=False):
        color = "red" if es_error else "green"
        self.lbl_mensaje.configure(text=mensaje, text_color=color)