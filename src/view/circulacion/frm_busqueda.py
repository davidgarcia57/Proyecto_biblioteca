import customtkinter as ctk
from tkinter import ttk

class FrmBusqueda(ctk.CTkToplevel):
    def __init__(self, master, callback_seleccion, tipo="libro"):
        super().__init__(master)
        self.callback = callback_seleccion
        self.tipo = tipo 
        self.funcion_busqueda = None # Aquí guardaremos la función del controller
        
        titulo = "Buscar Libro (Ejemplar)" if tipo == "libro" else "Buscar Lector"
        self.title(titulo)
        self.geometry("700x450")
        
        self.grab_set()
        self.focus_force()

        # --- BARRA SUPERIOR ---
        frm_top = ctk.CTkFrame(self, fg_color="transparent")
        frm_top.pack(fill="x", padx=20, pady=20)
        
        self.entry_busqueda = ctk.CTkEntry(frm_top, placeholder_text=f"Buscar {tipo}...", width=400, height=40)
        self.entry_busqueda.pack(side="left", padx=(0, 10))
        
        # Bindeamos Enter para buscar
        self.entry_busqueda.bind("<Return>", self.evento_buscar) 
        
        self.btn_buscar = ctk.CTkButton(frm_top, text="🔍 Buscar", width=100, height=40, 
                                        fg_color="#A7744A", command=self.evento_buscar)
        self.btn_buscar.pack(side="left")

        # --- TABLA ---
        frm_tabla = ctk.CTkFrame(self, fg_color="transparent")
        frm_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        if self.tipo == "libro":
            cols = ("ID", "Título", "Autor")
            anchos = (60, 350, 200)
        else:
            cols = ("ID", "Nombre", "Teléfono")
            anchos = (60, 350, 150)

        self.tree = ttk.Treeview(frm_tabla, columns=cols, show="headings")
        
        for i, col in enumerate(cols):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=anchos[i])

        scroll = ttk.Scrollbar(frm_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        
        self.tree.bind("<Double-1>", self.al_seleccionar)
        self.after(100, self.entry_busqueda.focus)

    def configurar_busqueda(self, funcion_del_controlador):
        """
        Permite al controlador inyectar su lógica de búsqueda BD.
        La función recibida debe aceptar un argumento (el término).
        """
        self.funcion_busqueda = funcion_del_controlador

    def evento_buscar(self, event=None):
        """Dispara la función inyectada por el controlador."""
        if self.funcion_busqueda:
            termino = self.entry_busqueda.get()
            self.funcion_busqueda(termino)

    def cargar_datos(self, lista_tuplas):
        """Método público para que el controlador llene la tabla."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in lista_tuplas:
            self.tree.insert("", "end", values=item)

    def al_seleccionar(self, event):
        """Retorna el ID seleccionado a la ventana padre mediante callback."""
        item = self.tree.selection()
        if item:
            valores = self.tree.item(item, "values")
            id_sel = valores[0]
            self.callback(id_sel) 
            self.destroy()