import customtkinter as ctk
from tkinter import StringVar, ttk # <--- OJO: Necesitamos 'ttk' para la tabla

class FrmBuscarLibro(ctk.CTkFrame):
    
    # --- PALETA DE COLORES ---
    COLOR_FONDO = "#F3E7D2"
    COLOR_TEXTO = "#5a3b2e"
    COLOR_BOTON = "#A7744A"
    COLOR_HOVER = "#8c5e3c"
    
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller 
        
        self.configure(fg_color=self.COLOR_FONDO)
        
        # 1. VARIABLE DE CONTROL (Búsqueda en Vivo)
        self.texto_busqueda = StringVar(value="")
        self.texto_busqueda.trace_add("write", self.al_escribir)
        self.id_busqueda_programada = None 
        
        # Grid principal 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # La fila 2 (tabla) es la que se estira

        # --- COMPONENTES ---
        self.crear_header()
        self.crear_elementos_busqueda()
        self.crear_tabla_resultados()

    def crear_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        
        self.btn_volver = ctk.CTkButton(
            header_frame,
            text="⬅ Volver al Menú",
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            text_color=self.COLOR_BOTON,
            border_width=2,
            border_color=self.COLOR_BOTON,
            hover_color=self.COLOR_FONDO,
            width=100,
            command=self.volver_menu
        )
        self.btn_volver.pack(side="left")

        lbl_titulo = ctk.CTkLabel(
            header_frame, 
            text="Catálogo de Libros", 
            font=("Georgia", 26, "bold"), 
            text_color=self.COLOR_TEXTO
        )
        lbl_titulo.pack(side="left", padx=20)

    def crear_elementos_busqueda(self):
        frame_busqueda = ctk.CTkFrame(self, fg_color="transparent")
        frame_busqueda.grid(row=1, column=0, sticky="n", pady=30)
        
        self.txt_busqueda = ctk.CTkEntry(
            frame_busqueda, 
            textvariable=self.texto_busqueda, # Conectado al StringVar
            placeholder_text="Título, Autor o ISBN del libro...",
            height=40,
            width=400,
            fg_color="white", 
            text_color="black",
            border_color=self.COLOR_BOTON,
            border_width=2,
            font=("Arial", 14)
        )
        self.btn_limpiar = ctk.CTkButton(
            frame_busqueda, text="X", width=40, height=40,
            fg_color="#D32F2F", hover_color="#B71C1C",
            font=("Arial", 14, "bold"),
            command=self.limpiar_busqueda
        )
        self.btn_limpiar.grid(row=0, column=2, padx=5) # Columna 2 (al lado de la lupa)
        self.txt_busqueda.grid(row=0, column=0, padx=(0, 10))

        # Botón opcional de momento
        self.btn_buscar = ctk.CTkButton(
            frame_busqueda,
            text="🔍",
            width=60,
            height=40,
            font=("Georgia", 14, "bold"),
            fg_color=self.COLOR_BOTON,
            hover_color=self.COLOR_HOVER,
            text_color="white",
            command=self.ejecutar_busqueda_ahora 
        )
        self.btn_buscar.grid(row=0, column=1)

    def limpiar_busqueda(self):
            self.txt_busqueda.delete(0, 'end') # Borra visualmente
            self.controller.realizar_busqueda("") # Fuerza búsqueda vacía (traer todo)
            
    # --- AQUÍ ESTABA LO QUE FALTABA: LA TABLA ---
    def crear_tabla_resultados(self):
        frame_tabla = ctk.CTkFrame(self, fg_color="transparent")
        frame_tabla.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Estilos para que la tabla combine con el diseño
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="white",
                        foreground=self.COLOR_TEXTO,
                        rowheight=30,
                        fieldbackground="white",
                        font=("Arial", 11))
        style.configure("Treeview.Heading", 
                        background=self.COLOR_BOTON,
                        foreground="white",
                        font=("Georgia", 12, "bold"))
        style.map("Treeview", background=[('selected', self.COLOR_HOVER)])

        columns = ("id", "titulo", "isbn", "autor", "anio", "editorial", "disp")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", selectmode="browse")
        
        # Encabezados
        self.tree.heading("id", text="ID")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("autor", text="Autor")
        self.tree.heading("anio", text="Año")
        self.tree.heading("editorial", text="Editorial")
        self.tree.heading("disp", text="Disponibilidad")

        # Columnas
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("titulo", width=250)
        self.tree.column("isbn", width=100)
        self.tree.column("autor", width=150)
        self.tree.column("anio", width=60, anchor="center")
        self.tree.column("editorial", width=120)
        self.tree.column("disp", width=120, anchor="center")

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # --- LÓGICA DE BÚSQUEDA EN VIVO ---
    def al_escribir(self, *args):
        if self.id_busqueda_programada:
            self.after_cancel(self.id_busqueda_programada)
        self.id_busqueda_programada = self.after(300, self.ejecutar_busqueda_ahora)

    def ejecutar_busqueda_ahora(self):
        termino = self.texto_busqueda.get()
        if self.controller:
            self.controller.realizar_busqueda(termino)

    def mostrar_resultados(self, lista_resultados):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if lista_resultados:
            for row in lista_resultados:
                # row viene así: (id, titulo, isbn, autor, editorial, disponibles, total)
                disponibles = row[5]
                total = row[6]
                
                estado_str = f"{disponibles} de {total} Disp."
                if disponibles == 0:
                    estado_str = "AGOTADO / PRESTADO"

                valores = (row[0], row[1], row[2], row[3], row[4], row[5], estado_str)
                
                # Truco visual: Si está agotado, podríamos pintarlo
                self.tree.insert("", "end", values=valores)
    def volver_menu(self):
        if self.controller:
            self.controller.volver_al_menu()