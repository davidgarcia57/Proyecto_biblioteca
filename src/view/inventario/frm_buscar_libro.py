import customtkinter as ctk
from tkinter import StringVar, ttk

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
        # HEADER AHORA SOLO TIENE EL BOTÓN DE VOLVER
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
        # (El título se movió de aquí)

    def crear_elementos_busqueda(self):
        frame_busqueda = ctk.CTkFrame(self, fg_color="transparent")
        frame_busqueda.grid(row=1, column=0, sticky="n", pady=(10, 30)) # Ajusté un poco el padding vertical
        
        # --- [CAMBIO] TÍTULO AQUÍ ---
        # Lo colocamos en la fila 0, alineado a la izquierda ("w")
        self.lbl_titulo = ctk.CTkLabel(
            frame_busqueda, 
            text="Catálogo de Libros", 
            font=("Georgia", 32, "bold"), # Hice la letra un poco más grande
            text_color=self.COLOR_TEXTO
        )
        # columnspan=3 permite que el título ocupe el ancho de la barra + botones si es largo
        self.lbl_titulo.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        # --- CAJA DE BÚSQUEDA (Mochila a Fila 1) ---
        self.txt_busqueda = ctk.CTkEntry(
            frame_busqueda, 
            textvariable=self.texto_busqueda,
            placeholder_text="Título, Autor o ISBN del libro...",
            height=40,
            width=400,
            fg_color="white", 
            text_color="black",
            border_color=self.COLOR_BOTON,
            border_width=2,
            font=("Arial", 14)
        )
        self.txt_busqueda.grid(row=1, column=0, padx=(0, 10))

        # --- BOTONES (Mochila a Fila 1) ---
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
        self.btn_buscar.grid(row=1, column=1)

        self.btn_agregar = ctk.CTkButton(
            frame_busqueda,
            text="+",
            width=40,
            height=40,
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            font=("Arial", 20, "bold"),
            command=self.evento_agregar
        )
        self.btn_agregar.grid(row=1, column=2, padx=5)
            
    def crear_tabla_resultados(self):
        frame_tabla = ctk.CTkFrame(self, fg_color="transparent")
        frame_tabla.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
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
        
        self.tree.heading("id", text="ID")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("autor", text="Autor")
        self.tree.heading("anio", text="Año")
        self.tree.heading("editorial", text="Editorial")
        self.tree.heading("disp", text="Disponibilidad")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("titulo", width=250)
        self.tree.column("isbn", width=100)
        self.tree.column("autor", width=150)
        self.tree.column("anio", width=60, anchor="center")
        self.tree.column("editorial", width=120)
        self.tree.column("disp", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", self.evento_doble_clic)

    # --- LÓGICA DE BÚSQUEDA ---
    def al_escribir(self, *args):
        if self.id_busqueda_programada:
            self.after_cancel(self.id_busqueda_programada)
        self.id_busqueda_programada = self.after(300, self.ejecutar_busqueda_ahora)

    def ejecutar_busqueda_ahora(self):
        termino = self.texto_busqueda.get()
        if self.controller:
            self.controller.realizar_busqueda(termino)

    def mostrar_resultados(self, lista_resultados):
        self.tree.delete(*self.tree.get_children())
            
        if lista_resultados:
            for row in lista_resultados:
                id_obra = row[0]
                titulo = row[1]
                isbn = row[2] if row[2] else ""
                autor = row[3] if row[3] else "Desconocido"
                anio = row[4] if row[4] else ""
                editorial = row[5] if row[5] else "Sin Editorial"
                disponibles = row[6]
                total = row[7]
                
                estado_str = f"{disponibles} de {total} Disp."
                if disponibles == 0:
                    estado_str = "AGOTADO / PRESTADO"

                valores = (id_obra, titulo, isbn, autor, anio, editorial, estado_str)
                self.tree.insert("", "end", values=valores)

    def volver_menu(self):
        if self.controller:
            self.controller.volver_al_menu()

    def evento_doble_clic(self, event):
        item_id = self.tree.selection()
        if item_id:
            item = self.tree.item(item_id)
            valores = item['values']
            id_obra = valores[0]
            if self.controller:
                self.controller.abrir_ficha_libro(id_obra)

    def evento_agregar(self):
        if self.controller:
            self.controller.ir_a_agregar_libro()