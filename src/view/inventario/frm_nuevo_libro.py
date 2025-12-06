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
        
        # Lista para almacenar las referencias a los checkboxes de ilustraciones
        self.checks_ilustracion = []

        # --- HEADER (Título fijo) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=40, pady=(20, 10))
        # --- BOTÓN VOLVER (NUEVO) ---
        self.btn_volver = ctk.CTkButton(
            self.header_frame,
            text="⬅ Volver",
            font=("Arial", 14, "bold"),
            fg_color="transparent",        
            text_color=self.COLOR_BOTON,  
            border_width=2,                
            border_color=self.COLOR_BOTON, 
            hover_color=self.COLOR_HOVER,  
            width=100,
            command=self.controller.volver_al_menu 
        )
        self.btn_volver.pack(side="left", padx=(0, 20))
        #------------------------------------------------------
        self.lbl_titulo_main = ctk.CTkLabel(
            self.header_frame, 
            text="Ficha de Ingreso de Libros ", 
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
    def validar_campo(self, entry_widget):
        """Retorna True si tiene texto, False si está vacío y lo pinta de rojo"""
        if not entry_widget.get().strip():
            entry_widget.configure(border_color="red")
            return False
        else:
            entry_widget.configure(border_color=self.COLOR_BOTON) 
            return True
        
    def crear_encabezado_paso(self, parent, texto):
        """Crea el título con la línea divisoria abajo"""
        frame_titulo = ctk.CTkFrame(parent, fg_color="transparent")
        frame_titulo.pack(fill="x", pady=(0, 20))

        lbl = ctk.CTkLabel(
            frame_titulo, 
            text=texto, 
            font=("Georgia", 20, "bold"), 
            text_color=self.COLOR_TEXTO
        )
        lbl.pack(side="left", anchor="w")

        linea = ctk.CTkFrame(parent, height=2, fg_color=self.COLOR_LINEA)
        linea.pack(fill="x", pady=(0, 20))

    def crear_input(self, parent, label_text, row, col, colspan=1):
        """Helper para crear labels y entries"""
        lbl = ctk.CTkLabel(
            parent, 
            text=label_text, 
            font=("Georgia", 12, "bold"), 
            text_color=self.COLOR_TEXTO 
        )
        lbl.grid(row=row, column=col, sticky="w", pady=(10, 5), padx=10)
        
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
    # DEFINICIÓN DE PASOS (Basado en la Ficha)
    # ==========================================

    def crear_paso_1(self):
        # PASO 1: Datos de Control y Clasificación
        self.frm_step1 = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frm_step1.columnconfigure((0, 1), weight=1)
        
        self.crear_encabezado_paso(self.frm_step1, "1. Datos de Ficha y Clasificación")
        
        grid_frame = ctk.CTkFrame(self.frm_step1, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.columnconfigure((0, 1), weight=1)

        # Fila 0: Ficha y ISBN
        self.entry_ficha = self.crear_input(grid_frame, "Ficha No. *", 0, 0)
        self.entry_isbn = self.crear_input(grid_frame, "ISBN", 0, 1)

        # Fila 2: Clasificación
        self.entry_clasif = self.crear_input(grid_frame, "Clasificación *", 2, 0, colspan=2)
        
        # --- SECCIÓN DE CÓDIGO DE ILUSTRACIONES (CHECKBOXES) ---
        lbl_ilus = ctk.CTkLabel(grid_frame, text="Código de ilustraciones (Selección Múltiple)", font=("Georgia", 12, "bold"), text_color=self.COLOR_TEXTO)
        lbl_ilus.grid(row=4, column=0, sticky="w", padx=10, pady=(10,0))
        
        # Usamos ScrollableFrame para que quepan todas las opciones
        self.scroll_ilustraciones = ctk.CTkScrollableFrame(
            grid_frame, 
            height=150, 
            width=300, 
            fg_color="white", 
            border_color=self.COLOR_BOTON, 
            border_width=1,
            label_text="Opciones Disponibles",
            label_text_color=self.COLOR_TEXTO
        )
        self.scroll_ilustraciones.grid(row=5, column=0, sticky="ew", padx=10, pady=(5,10))
        
        # Lista completa
        opciones = [
            "X - Sin ilustraciones", "A - Ilustraciones", "B - Mapa", "C - Retratos", 
            "D - Fotografías", "E - Planos", "F - Láminas", "G - Música", 
            "H - Facsímiles", "I - Diagramas", "J - Grabados", "K - Litografía",
            "L - Grabaciones o discos", "M - Gráficas", "N - Tablas", "P - Laminaciones",
            "Q - Diskettes", "R - Tablas Genealógicas", "S - Dispositivas", 
            "T - Formas y formularios", "U - Muestras", "Z - Otros"
        ]
        
        # Generamos los checkboxes dinámicamente
        self.checks_ilustracion = []
        for op in opciones:
            chk = ctk.CTkCheckBox(
                self.scroll_ilustraciones, 
                text=op, 
                text_color="black",
                fg_color=self.COLOR_BOTON, 
                hover_color=self.COLOR_HOVER
            )
            chk.pack(anchor="w", pady=2, padx=5)
            self.checks_ilustracion.append(chk)

        frame_idioma = ctk.CTkFrame(grid_frame, fg_color="transparent")
        frame_idioma.grid(row=4, column=1, sticky="nsew", padx=10, pady=(10,0))

        lbl_idioma = ctk.CTkLabel(
            frame_idioma,
            text="Código de Lengua",
            font=("Georgia", 12, "bold"),
            text_color=self.COLOR_TEXTO
        )
        lbl_idioma.pack(anchor="w")

        self.entry_idioma = ctk.CTkEntry(
            frame_idioma,
            placeholder_text="Código de Lengua",
            fg_color="white",
            text_color="black",
            border_color=self.COLOR_BOTON,
            height=35
        )
        self.entry_idioma.pack(fill="x", pady=(5,0))
        self.entry_idioma.insert(0, "Español")


    def crear_paso_2(self):
        # PASO 2: Autoría y Título
        self.frm_step2 = ctk.CTkFrame(self.container, fg_color="transparent")
        self.crear_encabezado_paso(self.frm_step2, "2. Autoría y Título")

        grid_frame = ctk.CTkFrame(self.frm_step2, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.columnconfigure((0, 1), weight=1)

        self.entry_autor = self.crear_input(grid_frame, "Autor Personal (Principal) *", 0, 0, colspan=2)
        self.entry_autor_corp = self.crear_input(grid_frame, "Autor Corporativo", 2, 0, colspan=2)
        self.entry_titulo = self.crear_input(grid_frame, "Título / Mención de responsabilidad *", 4, 0, colspan=2)
        self.entry_asientos = self.crear_input(grid_frame, "Asientos Secundarios (Coautores)", 6, 0, colspan=2)


    def crear_paso_3(self):
        # PASO 3: Edición, Publicación y Descripción
        self.frm_step3 = ctk.CTkFrame(self.container, fg_color="transparent")
        self.crear_encabezado_paso(self.frm_step3, "3. Edición, Publicación y Descripción")

        grid_frame = ctk.CTkFrame(self.frm_step3, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.columnconfigure((0, 1), weight=1)

        self.entry_edicion = self.crear_input(grid_frame, "Mención de Edición", 0, 0)
        self.entry_anio = self.crear_input(grid_frame, "Fecha de publicación", 0, 1)
        self.entry_lugar = self.crear_input(grid_frame, "Lugar de publicación", 2, 0)
        self.entry_editorial = self.crear_input(grid_frame, "Editorial", 2, 1)
        self.entry_paginas = self.crear_input(grid_frame, "Páginas, volumen, etc.", 4, 0)
        self.entry_dimensiones = self.crear_input(grid_frame, "Dimensiones (cm)", 4, 1)
        self.entry_serie = self.crear_input(grid_frame, "Serie", 6, 0, colspan=2)
        self.entry_descripcion = self.crear_input(grid_frame, "Notas Generales / Historial", 8, 0)


    def crear_paso_4(self):
        # PASO 4: Ejemplares y Auditoría
        self.frm_step4 = ctk.CTkFrame(self.container, fg_color="transparent")
        self.crear_encabezado_paso(self.frm_step4, "4. Ejemplares y Auditoría")

        grid_frame = ctk.CTkFrame(self.frm_step4, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.columnconfigure((0, 1), weight=1)

        self.entry_ubicacion = self.crear_input(grid_frame, "Ubicación (Ej. Biblioteca)", 0, 0)
        self.entry_ubicacion.insert(0, "General")

        self.entry_numero_copia = self.crear_input(grid_frame, "Ejemplar (Ej. Copia 1)", 0, 1)
        self.entry_numero_copia.insert(0, "Copia 1")
        
        self.entry_tomo = self.crear_input(grid_frame, "Tomo (Opcional)", 4, 0)
        self.entry_volumen = self.crear_input(grid_frame, "Volumen (Opcional)", 4, 1)


    # ==========================================
    # NAVEGACIÓN Y GUARDADO
    # ==========================================

    def mostrar_paso(self, index):
        for step in self.steps:
            step.pack_forget()
        
        self.steps[index].pack(fill="both", expand=True)
        self.lbl_paginacion.configure(text=f"Paso {index + 1} de {len(self.steps)}")

        #NUEVO BLOQUE DE CODIGO
        if index == 0:
            # Si estamos en el paso 1, el botón de arriba saca al menú
            self.btn_volver.configure(text="⬅ Volver al Menú", command=self.controller.volver_al_menu)
        else:
            # Si estamos en pasos avanzados, el botón de arriba regresa uno atrás
            self.btn_volver.configure(text="⬅ Paso Anterior", command=self.anterior_paso)
        #------------
        if index == 0:
            self.btn_atras.configure(text="Cancelar", fg_color="#D32F2F", hover_color="#B71C1C", state="normal")
        else:
            self.btn_atras.configure(text="Atrás", fg_color="gray", hover_color="#666666", state="normal")

        if index == len(self.steps) - 1:
            self.btn_siguiente.configure(text="GUARDAR FICHA", fg_color="#2E7D32")
        else:
            self.btn_siguiente.configure(text="Siguiente", fg_color=self.COLOR_BOTON)

    def siguiente_paso(self):
        # VALIDACIONES
        if self.current_step == 0:
            if not self.validar_campo(self.entry_ficha):
                self.mostrar_mensaje("El No. de Ficha es obligatorio", True)
                return
            if not self.validar_campo(self.entry_clasif):
                self.mostrar_mensaje("La Clasificación es obligatoria", True)
                return

        if self.current_step == 1:
            if not self.validar_campo(self.entry_autor):
                self.mostrar_mensaje("El Autor Personal es obligatorio", True)
                return
            if not self.validar_campo(self.entry_titulo):
                self.mostrar_mensaje("El Título es obligatorio", True)
                return

        if self.current_step == len(self.steps) - 1:
            self.evento_guardar()
        else:
            self.current_step += 1
            self.mostrar_paso(self.current_step)
            self.mostrar_mensaje("")

    def anterior_paso(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.mostrar_paso(self.current_step)
        else:
            self.controller.volver_al_menu()
            
    def evento_guardar(self):
        # 1. Recolectar Códigos de Ilustración
        codigos_seleccionados = []
        for chk in self.checks_ilustracion:
            if chk.get() == 1: # Si está marcado
                # Obtenemos solo la letra inicial (ej. "A" de "A - Ilustraciones")
                texto_completo = chk.cget("text")
                letra = texto_completo.split(" - ")[0] 
                codigos_seleccionados.append(letra)
        
        # Unimos con comas: "A,B,M"
        str_ilustraciones = ",".join(codigos_seleccionados)

        # 2. Recolectar resto de datos
        datos = {
            "ficha_no": self.entry_ficha.get(),
            "isbn": self.entry_isbn.get(),
            "clasificacion": self.entry_clasif.get(),
            "codigo_ilustracion": str_ilustraciones, # Enviamos la cadena
            "idioma": self.entry_idioma.get(),
            
            "autor_nombre": self.entry_autor.get(),
            "autor_corporativo": self.entry_autor_corp.get(),
            "titulo": self.entry_titulo.get(),
            "asientos_secundarios": self.entry_asientos.get(),
            
            "edicion": self.entry_edicion.get(),
            "anio": self.entry_anio.get(),
            "lugar_publicacion": self.entry_lugar.get(),
            "editorial_nombre": self.entry_editorial.get(),
            "paginas": self.entry_paginas.get(),
            "dimensiones": self.entry_dimensiones.get(),
            "serie": self.entry_serie.get(),
            "descripcion": self.entry_descripcion.get(),
            "ubicacion": self.entry_ubicacion.get(),
            "numero_copia": self.entry_numero_copia.get(),
            "tomo": self.entry_tomo.get(),
            "volumen": self.entry_volumen.get()
        }
        self.controller.registrar_libro_completo(datos)

    def limpiar_formulario(self):
        """Resetea todos los campos al estado inicial para un nuevo registro"""
        # 1. Lista de todos los campos de texto
        campos = [
            self.entry_ficha, self.entry_isbn, self.entry_clasif, 
            self.entry_autor, self.entry_autor_corp, self.entry_titulo, self.entry_asientos,
            self.entry_edicion, self.entry_anio, self.entry_lugar, self.entry_editorial,
            self.entry_paginas, self.entry_dimensiones, self.entry_serie, self.entry_descripcion,
            self.entry_tomo, self.entry_volumen
        ]
        
        # Limpiamos texto normal
        for campo in campos:
            campo.delete(0, 'end')
            campo.configure(border_color=self.COLOR_BOTON) # Resetear color rojo si hubo error

        # 2. Resetear campos con valores por defecto
        self.entry_idioma.delete(0, 'end')
        self.entry_idioma.insert(0, "Español")
        
        self.entry_ubicacion.delete(0, 'end')
        self.entry_ubicacion.insert(0, "General")
        
        self.entry_numero_copia.delete(0, 'end')
        self.entry_numero_copia.insert(0, "Copia 1")

        # 3. Desmarcar todos los checkboxes
        for chk in self.checks_ilustracion:
            chk.deselect()

        # 4. Volver al paso 1
        self.current_step = 0
        self.mostrar_paso(0)
        self.lbl_mensaje.configure(text="") # Limpiar mensaje inferior si hubiera

    def confirmar_registro(self, id_generado):
        """Muestra popup de éxito y pregunta si desea continuar"""
        respuesta = messagebox.askyesno(
            "Registro Exitoso",
            f"¡Libro guardado correctamente!\n\nNo. Adquisición Asignado: {id_generado}\n\n¿Desea registrar otro libro ahora?"
        )
        
        if respuesta: # Si dice SÍ (True)
            self.limpiar_formulario()
        else: # Si dice NO (False)
            self.controller.volver_al_menu()


    def mostrar_mensaje(self, mensaje, es_error=False):
        color = "red" if es_error else "#2E7D32"
        self.lbl_mensaje.configure(text=mensaje, text_color=color)