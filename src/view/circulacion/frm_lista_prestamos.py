import customtkinter as ctk
from tkinter import ttk, messagebox
from src.model.Prestamo import Prestamo

class FrmListaPrestamos(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="#F3E7D2") # Beige
        
        # Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkButton(header, text="⬅ Volver", width=80, fg_color="#A7744A", 
                      command=self.controller.volver_menu).pack(side="left")
        
        ctk.CTkLabel(header, text="Préstamos Activos (Pendientes)", font=("Georgia", 24, "bold"), 
                     text_color="#5a3b2e").pack(side="left", padx=20)

        # Tabla
        panel_tabla = ctk.CTkFrame(self, fg_color="white")
        panel_tabla.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,10))

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        
        # Agregamos "id_ejemplar" como columna, aunque no la mostraremos en displaycolumns si quisieramos ocultarla
        # pero es más fácil ponerle width=0
        columns = ("ID", "Solicitante", "Libro", "Vence", "id_ejemplar")
        self.tree = ttk.Treeview(panel_tabla, columns=columns, show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Solicitante", text="Solicitante")
        self.tree.heading("Libro", text="Libro Prestado")
        self.tree.heading("Vence", text="Fecha Vencimiento")
        self.tree.heading("id_ejemplar", text="") # Oculto
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Solicitante", width=250)
        self.tree.column("Libro", width=350)
        self.tree.column("Vence", width=120, anchor="center")
        self.tree.column("id_ejemplar", width=0, stretch=False) # Columna oculta
        
        self.tree.pack(fill="both", expand=True)
        
        # --- NUEVO: Botón de Devolución ---
        btn_devolver = ctk.CTkButton(
            self, 
            text="✅ Devolver Libro Seleccionado", 
            fg_color="#2E7D32", 
            height=50, 
            font=("Arial", 14, "bold"),
            command=self.evento_devolver
        )
        btn_devolver.grid(row=2, column=0, pady=20, padx=20, sticky="ew")

        # Cargar datos
        self.cargar_datos()

    def cargar_datos(self):
        datos = Prestamo.obtener_activos()
        # Limpiar
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Llenar
        for row in datos:
            # row: (id_prestamo, solicitante, libro, fecha_vence, id_ejemplar)
            self.tree.insert("", "end", values=row)

    def evento_devolver(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un préstamo de la lista para devolver.")
            return
        
        item = self.tree.item(seleccion)
        valores = item['values']
        
        id_prestamo = valores[0]
        libro_titulo = valores[2]
        id_ejemplar = valores[4] # Dato oculto
        
        if messagebox.askyesno("Confirmar Devolución", f"¿Confirmar la devolución del libro?\n\n'{libro_titulo}'"):
            self.controller.procesar_devolucion(id_prestamo, id_ejemplar)