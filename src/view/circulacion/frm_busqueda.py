import customtkinter as ctk
from tkinter import ttk

class FrmBusqueda(ctk.CTkToplevel):
    def __init__(self, master, callback_seleccion, tipo="libro"):
        super().__init__(master)
        self.callback = callback_seleccion
        self.tipo = tipo # "libro" o "lector"
        
        titulo = "Buscar Libro (Ejemplar)" if tipo == "libro" else "Buscar Lector"
        self.title(titulo)
        self.geometry("700x450")
        
        # Modal
        self.grab_set()
        self.focus_force()

        # --- BARRA SUPERIOR ---
        frm_top = ctk.CTkFrame(self, fg_color="transparent")
        frm_top.pack(fill="x", padx=20, pady=20)
        
        self.entry_busqueda = ctk.CTkEntry(frm_top, placeholder_text=f"Buscar {tipo}...", width=400, height=40)
        self.entry_busqueda.pack(side="left", padx=(0, 10))
        self.entry_busqueda.bind("<Return>", self.ejecutar_busqueda_evento) # Enter para buscar
        
        btn_buscar = ctk.CTkButton(frm_top, text="🔍 Buscar", width=100, height=40, 
                                   fg_color="#A7744A", command=self.ejecutar_busqueda_evento)
        btn_buscar.pack(side="left")

        # --- TABLA DE RESULTADOS ---
        frm_tabla = ctk.CTkFrame(self, fg_color="transparent")
        frm_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Definir columnas según el tipo
        if self.tipo == "libro":
            cols = ("ID", "Título", "Autor")
            anchos = (60, 350, 200)
        else:
            cols = ("ID", "Nombre", "Teléfono")
            anchos = (60, 350, 150)

        self.tree = ttk.Treeview(frm_tabla, columns=cols, show="headings")
        
        # Configurar encabezados
        for i, col in enumerate(cols):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=anchos[i])

        # Scrollbar
        scroll = ttk.Scrollbar(frm_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        
        # Doble clic selecciona
        self.tree.bind("<Double-1>", self.al_seleccionar)

        # Carga inicial vacía o sugerida (opcional)
        self.after(100, self.entry_busqueda.focus)

    def ejecutar_busqueda_evento(self, event=None):
        # Este método será sobrescrito o asignado por el controlador,
        # pero por diseño, la vista dispara un evento que el controlador escucha.
        # En este caso simple, usaremos un método inyectado si existe, o dejaremos que el controller maneje la logica
        # pasando la referencia.
        # PERO, para mantener el patrón MVC limpio como en tu proyecto:
        # El controlador asignará el comando al botón. Aquí solo facilitamos el "bind".
        pass 

    def cargar_datos(self, lista_tuplas):
        """Limpia y llena la tabla"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in lista_tuplas:
            self.tree.insert("", "end", values=item)

    def al_seleccionar(self, event):
        item = self.tree.selection()
        if item:
            valores = self.tree.item(item, "values")
            id_sel = valores[0]
            self.callback(id_sel) # Llamamos a la función que nos pasó el Controlador
            self.destroy()