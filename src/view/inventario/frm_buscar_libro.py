import customtkinter as ctk
from tkinter import StringVar

class FmrBuscarLibro(ctk.CTkFrame):
    
    # --- PALETA DE COLORES ---
    COLOR_FONDO = "#F3E7D2"
    COLOR_TEXTO = "#5a3b2e"
    COLOR_BOTON = "#A7744A"
    COLOR_HOVER = "#8c5e3c"
    
    def __init__(self, master, controller=None):
    # Esto hace que funsione el Frame y aqui ponemos el color de fondo 
    # y preparamos el texto para que se guarde lo que escribira el usuario
        super().__init__(master)
        self.controller = controller 
        
        self.configure(fg_color=self.COLOR_FONDO)
        self.texto_busqueda = StringVar(value="")
        
        self.crear_elementos_busqueda()

    def crear_elementos_busqueda(self):
        # Este metodo tiene las instruciones para dibujar las caja de texto y boton
        # y aqui organizara su posicion dentro del Frame usando grid
        
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0) 

        self.txt_busqueda = ctk.CTkEntry(
            self, 
            textvariable=self.texto_busqueda,
            placeholder_text="Título, Autor o ISBN del libro...",
            height=40,
            fg_color="white", 
            text_color="black",
            border_color=self.COLOR_BOTON,
            border_width=2,
            font=("Arial", 16)
        )
        self.txt_busqueda.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="ew")

        self.btn_buscar = ctk.CTkButton(
            self,
            text="🔍 BUSCAR",
            width=150,
            height=40,
            font=("Georgia", 16, "bold"),
            fg_color=self.COLOR_BOTON,
            hover_color=self.COLOR_HOVER,
            text_color="white",
            command=self.placeholder_funcion_buscar 
        )
        self.btn_buscar.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="e")
        
        
    def placeholder_funcion_buscar(self):
        # Este método se ejecuta cuando se presiona el botón "BUSCAR".
        # Aquí se conectará la lógica real de búsqueda en el futuro.
        termino = self.texto_busqueda.get() 
        print(f"Botón Buscar presionado. Se buscaría el término: {termino}")