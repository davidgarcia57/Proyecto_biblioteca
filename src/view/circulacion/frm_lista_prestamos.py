import customtkinter as ctk
from tkinter import ttk, messagebox

class FrmListaPrestamos(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="#F3E7D2") 
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        ctk.CTkButton(header, text="⬅ Volver", width=150, height=50,
            font=("Arial", 18, "bold"), fg_color="#A7744A", 
            command=self.controller.volver_menu
        ).pack(side="left")
        
        ctk.CTkLabel(header, text="Préstamos Activos", 
            font=("Arial", 32, "bold"), text_color="#000000"
        ).pack(side="left", padx=30)

        panel_tabla = ctk.CTkFrame(self, fg_color="white")
        panel_tabla.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,10))

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14), rowheight=40)
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
        
        columns = ("ID", "Solicitante", "Libro", "Vence", "id_ejemplar")
        self.tree = ttk.Treeview(panel_tabla, columns=columns, show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Solicitante", text="Solicitante")
        self.tree.heading("Libro", text="Libro Prestado")
        self.tree.heading("Vence", text="Vence") 
        self.tree.heading("id_ejemplar", text="ID Ejemplar") 
        
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Solicitante", width=300)
        self.tree.column("Libro", width=400)
        self.tree.column("Vence", width=150, anchor="center")
        self.tree.column("id_ejemplar", width=0, stretch=False) 
        
        scrollbar = ctk.CTkScrollbar(panel_tabla, command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(fill="both", expand=True)
        
        ctk.CTkButton(self, text="✅ Devolver Libro Seleccionado", 
            fg_color="#2E7D32", height=60, font=("Arial", 20, "bold"), 
            command=self.evento_devolver
        ).grid(row=2, column=0, pady=20, padx=20, sticky="ew")

    def actualizar_tabla(self, datos):
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in datos:
            self.tree.insert("", "end", values=row)

    def evento_devolver(self):

        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un préstamo de la lista.")
            return
        
        item = self.tree.item(seleccion)
        valores = item['values']
        
        self.controller.procesar_devolucion(valores[0], valores[4])