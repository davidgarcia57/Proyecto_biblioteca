import customtkinter as ctk
from tkinter import StringVar, ttk

class FrmBuscarLibro(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller 
        
        self.configure(fg_color="#F3E7D2")
        
        # Grid: 30% Instrucciones (Izq) | 70% Tabla (Der)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=7)
        self.grid_rowconfigure(1, weight=1)

        self.texto_busqueda = StringVar(value="")
        self.texto_busqueda.trace_add("write", self.al_escribir)
        self.id_busqueda_programada = None 

        # --- HEADER ---
        self.crear_header()

        # --- PANELES ---
        self.crear_panel_instrucciones(row=1, col=0)
        self.crear_panel_catalogo(row=1, col=1)

    def crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(20, 10))
        
        btn_volver = ctk.CTkButton(
            header, text="⬅ VOLVER AL MENÚ", width=220, height=55,
            fg_color="#8D6E63", hover_color="#6D4C41",
            font=("Arial", 18, "bold"), command=self.volver_menu
        )
        btn_volver.pack(side="left")
        
        ctk.CTkLabel(header, text="CATÁLOGO DE LIBROS", font=("Georgia", 32, "bold"), text_color="#5a3b2e").pack(side="left", padx=40)

    def crear_panel_instrucciones(self, row, col):
        p_inst = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_color="#Decdbb", border_width=2)
        p_inst.grid(row=row, column=col, sticky="nsew", padx=(30, 10), pady=20)
        
        container = ctk.CTkFrame(p_inst, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=20)
        
        ctk.CTkLabel(container, text="GESTIÓN DE OBRAS", font=("Arial", 26, "bold"), text_color="#A7744A").pack(pady=(0, 30))
        
        texto = (
            "🔍 BÚSQUEDA:\n"
            "Escriba el título, autor o ISBN en la barra\n"
            "superior derecha.\n\n"
            "✏️ EDICIÓN:\n"
            "Haga DOBLE CLIC sobre cualquier libro\n"
            "de la tabla para editar sus datos.\n\n"
            "➕ NUEVO:\n"
            "Use el botón verde para registrar\n"
            "una nueva adquisición."
        )
        
        ctk.CTkLabel(container, text=texto, font=("Arial", 20), text_color="#333333", justify="center").pack(anchor="center")
        
        # Botón Nuevo Libro (Movido aquí para mejor acceso)
        ctk.CTkButton(container, text="➕ REGISTRAR NUEVO LIBRO", width=250, height=60,
                      fg_color="#2E7D32", hover_color="#1B5E20", font=("Arial", 16, "bold"),
                      command=self.evento_agregar).pack(side="bottom", pady=40)

    def crear_panel_catalogo(self, row, col):
        p_cat = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        p_cat.grid(row=row, column=col, sticky="nsew", padx=(10, 30), pady=20)
        
        # Barra de Búsqueda
        f_top = ctk.CTkFrame(p_cat, fg_color="transparent")
        f_top.pack(fill="x", padx=20, pady=20)
        
        self.txt_busqueda = ctk.CTkEntry(f_top, textvariable=self.texto_busqueda, placeholder_text="Escriba para buscar...",
                                         height=50, font=("Arial", 16))
        self.txt_busqueda.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(f_top, text="🔍 BUSCAR", width=120, height=50, fg_color="#A7744A",
                      font=("Arial", 14, "bold"), command=self.ejecutar_busqueda_ahora).pack(side="left")

        # Tabla
        f_tabla = ctk.CTkFrame(p_cat, fg_color="transparent")
        f_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Estilos Tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="black", rowheight=35, fieldbackground="white", font=("Arial", 12))
        style.configure("Treeview.Heading", background="#A7744A", foreground="white", font=("Arial", 14, "bold"))
        style.map("Treeview", background=[('selected', '#8c5e3c')])

        cols = ("id", "titulo", "isbn", "autor", "anio", "editorial", "disp")
        self.tree = ttk.Treeview(f_tabla, columns=cols, show="headings", selectmode="browse")
        
        cabeceras = {"id":"ID", "titulo":"Título", "isbn":"ISBN", "autor":"Autor", "anio":"Año", "editorial":"Edit.", "disp":"Estado"}
        anchos = {"id":50, "titulo":250, "isbn":100, "autor":150, "anio":60, "editorial":100, "disp":120}
        
        for c, t in cabeceras.items():
            self.tree.heading(c, text=t)
            self.tree.column(c, width=anchos[c])

        sb = ctk.CTkScrollbar(f_tabla, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", self.evento_doble_clic)

    # --- LÓGICA PRESERVADA ---
    def al_escribir(self, *args):
        if self.id_busqueda_programada: self.after_cancel(self.id_busqueda_programada)
        self.id_busqueda_programada = self.after(300, self.ejecutar_busqueda_ahora)

    def ejecutar_busqueda_ahora(self):
        if self.controller: self.controller.realizar_busqueda(self.texto_busqueda.get())

    def mostrar_resultados(self, lista):
        self.tree.delete(*self.tree.get_children())
        if lista:
            for row in lista:
                disp, tot = row[6], row[7]
                estado = f"{disp} de {tot} Disp." if disp > 0 else "AGOTADO"
                self.tree.insert("", "end", values=(row[0], row[1], row[2] or "", row[3] or "S/A", row[4] or "", row[5] or "", estado))

    def volver_menu(self):
        if self.controller: self.controller.volver_al_menu()

    def evento_doble_clic(self, event):
        item = self.tree.selection()
        if item and self.controller: self.controller.abrir_ficha_libro(self.tree.item(item)['values'][0])

    def evento_agregar(self):
        if self.controller: self.controller.ir_a_agregar_libro()