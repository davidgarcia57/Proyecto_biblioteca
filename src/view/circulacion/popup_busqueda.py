import customtkinter as ctk
from tkinter import ttk

class PopupBusqueda(ctk.CTkToplevel):
    def __init__(self, master, callback_seleccion, tipo="libro"):
        super().__init__(master)
        self.callback = callback_seleccion
        self.tipo = tipo # "libro" o "usuario"
        self.title(f"Buscar {tipo.capitalize()}")
        self.geometry("600x400")
        
        # Hacer la ventana modal (bloquea la de atrás)
        self.grab_set()
        self.focus_force()

        # Barra de búsqueda
        self.frm_top = ctk.CTkFrame(self)
        self.frm_top.pack(fill="x", padx=10, pady=10)
        
        self.entry_busqueda = ctk.CTkEntry(self.frm_top, placeholder_text="Escribe para buscar...", width=300)
        self.entry_busqueda.pack(side="left", padx=5)
        self.entry_busqueda.bind("<Return>", self.realizar_busqueda)
        
        btn_buscar = ctk.CTkButton(self.frm_top, text="Buscar", command=self.realizar_busqueda, width=100)
        btn_buscar.pack(side="left", padx=5)

        # Tabla de resultados
        self.tree = ttk.Treeview(self, columns=("id", "dato1", "dato2"), show="headings")
        self.tree.heading("id", text="ID")
        # Configurar columnas dinámicamente
        if tipo == "libro":
            self.tree.heading("dato1", text="Título")
            self.tree.heading("dato2", text="Autor / Estado")
        else:
            self.tree.heading("dato1", text="Nombre")
            self.tree.heading("dato2", text="Tipo / Contacto")
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Evento doble clic
        self.tree.bind("<Double-1>", self.on_double_click)

    def realizar_busqueda(self, event=None):
        termino = self.entry_busqueda.get()

        # aqui se debe llamar a la base de datos
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        # EJEMPLO SIMULADO (Debes conectarlo a tu controller/modelo real)
        if self.tipo == "libro":
            # Lo ideal es buscar EJEMPLARES disponibles, no solo Obras
            # SELECT id_ejemplar, titulo, autor FROM ... WHERE estado='Disponible'
            pass 
        
    def cargar_datos(self, lista_tuplas):
        """Método helper para llenar la tabla desde fuera"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in lista_tuplas:
            self.tree.insert("", "end", values=item)

    def on_double_click(self, event):
        item = self.tree.selection()
        if item:
            valores = self.tree.item(item, "values")
            id_seleccionado = valores[0]
            # Ejecutamos la función que nos pasaron y cerramos
            self.callback(id_seleccionado)
            self.destroy()