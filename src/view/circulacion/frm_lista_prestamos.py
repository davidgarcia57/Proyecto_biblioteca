import customtkinter as ctk
from tkinter import ttk, messagebox
from src.model.Prestamo import Prestamo

class FrmListaPrestamos(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="#F3E7D2") 
        
        # Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- HEADER ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        

        ctk.CTkButton(
            header, 
            text="⬅ Volver", 
            width=150,               # Más ancho para que sea fácil de apuntar
            height=50,               # Más alto
            font=("Arial", 18, "bold"), # Letra grande (18px)
            fg_color="#A7744A", 
            command=self.controller.volver_menu
        ).pack(side="left")
        
        # CAMBIO: Título más grande y tipografía Arial (más limpia que Georgia)
        ctk.CTkLabel(
            header, 
            text="Préstamos Activos", 
            font=("Arial", 32, "bold"), # Aumento de 24 a 32px
            text_color="#000000"        # Negro puro para máximo contraste
        ).pack(side="left", padx=30)

        # --- TABLA (TREEVIEW) ---
        panel_tabla = ctk.CTkFrame(self, fg_color="white")
        panel_tabla.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,10))

        # Configuración de Estilo para la Tabla (CRÍTICO)
        style = ttk.Style()
        
        # CAMBIO: Aumento drástico del tamaño de letra de la tabla y altura de fila
        style.configure(
            "Treeview", 
            font=("Arial", 18),   # De 11px a 18px (Regla de oro)
            rowheight=50          # De 25 a 50 (Espacio para dedo/mouse torpe)
        )
        
        # CAMBIO: Encabezados grandes
        style.configure(
            "Treeview.Heading", 
            font=("Arial", 20, "bold"), 
            padding=(5, 10)       # Un poco de aire en el encabezado
        )
        
        columns = ("ID", "Solicitante", "Libro", "Vence", "id_ejemplar")
        self.tree = ttk.Treeview(panel_tabla, columns=columns, show="headings")
        
        # Definición de encabezados
        self.tree.heading("ID", text="ID")
        self.tree.heading("Solicitante", text="Solicitante")
        self.tree.heading("Libro", text="Libro Prestado")
        self.tree.heading("Vence", text="Vence") # Texto más corto para ahorrar espacio visual
        self.tree.heading("id_ejemplar", text="") 
        
        # CAMBIO: Ajuste de anchos para la resolución 1024px con letra grande
        # Total disponible aprox ~980px.
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Solicitante", width=300)      # Más espacio
        self.tree.column("Libro", width=450)            # Más espacio
        self.tree.column("Vence", width=150, anchor="center")
        self.tree.column("id_ejemplar", width=0, stretch=False)
        
        # CAMBIO: Scrollbar (Vital para accesibilidad si la lista es larga)
        scrollbar = ctk.CTkScrollbar(panel_tabla, command=self.tree.yview, width=24) # Barra ancha
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(fill="both", expand=True)
        
        # --- BOTÓN DE ACCIÓN ---
        btn_devolver = ctk.CTkButton(
            self, 
            text="✅ Devolver Libro Seleccionado", 
            fg_color="#2E7D32", 
            height=70,                  # CAMBIO: Altura de 50 a 70 (Objetivo fácil)
            font=("Arial", 22, "bold"), # CAMBIO: Letra gigante para la acción principal
            command=self.evento_devolver
        )
        btn_devolver.grid(row=2, column=0, pady=20, padx=20, sticky="ew")

        # Cargar datos
        self.cargar_datos()

    def cargar_datos(self):
        # (Tu lógica original se mantiene igual)
        datos = Prestamo.obtener_activos()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in datos:
            self.tree.insert("", "end", values=row)

    def evento_devolver(self):
        # (Tu lógica original se mantiene igual)
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Por favor, seleccione un préstamo de la lista.") # Texto más amable
            return
        
        item = self.tree.item(seleccion)
        valores = item['values']
        id_prestamo = valores[0]
        libro_titulo = valores[2]
        id_ejemplar = valores[4]
        
        if messagebox.askyesno("Confirmar", f"¿Devolver este libro?\n\n📕 {libro_titulo}"):
            self.controller.procesar_devolucion(id_prestamo, id_ejemplar)